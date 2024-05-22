describe('Conflicting Orders', () => {
  const order1 = {
    name: 'User 1',
    contact: '11111111',
    creditCardNumber: '4111111111111111',
    expirationDate: '12/26',
    cvv: '123',
    street: 'Street 1',
    city: 'City 1',
    state: 'State 1',
    zip: '11111',
    country: 'Estonia',
    bookId: 3
  };

  const order2 = {
    name: 'User 2',
    contact: '22222222',
    creditCardNumber: '4111111111111111',
    expirationDate: '11/25',
    cvv: '456',
    street: 'Street 2',
    city: 'City 2',
    state: 'State 2',
    zip: '22222',
    country: 'Estonia',
    bookId: 3
  };

  it('should handle conflicting orders for the same book', () => {
    const visitAndFillOrder = (order) => {
      cy.visit(`http://localhost:8080/checkout/${order.bookId}`);
      cy.get('input[name="userName"]').type(order.name);
      cy.get('input[name="userContact"]').type(order.contact);
      cy.get('input[name="creditCardNumber"]').type(order.creditCardNumber);
      cy.get('input[name="creditCardExpirationDate"]').type(order.expirationDate);
      cy.get('input[name="creditCardCVV"]').type(order.cvv);
      cy.get('input[name="billingAddressStreet"]').type(order.street);
      cy.get('input[name="billingAddressCity"]').type(order.city);
      cy.get('input[name="billingAddressState"]').type(order.state);
      cy.get('input[name="billingAddressZip"]').type(order.zip);
      cy.get('select[name="billingAddressCountry"]').select(order.country);
      cy.get('input[name="termsAndConditionsAccepted"]').check();
    };

    const submitOrder = () => {
      cy.get('button[type="submit"]').click();
    };

    // Open the first order in a separate tab
    cy.window().then((win) => {
      const order1Page = win.open(`http://localhost:8080/checkout/${order1.bookId}`, '_blank', 'width=600,height=400');
      cy.wrap(order1Page).then((page) => {
        cy.stub(page, 'fetch')
          .callThrough()
          .withArgs(Cypress.sinon.match.has('url', `/checkout/${order1.bookId}`))
          .as('fetchOrder1');
      });
    });

    // Open the second order in another tab
    cy.window().then((win) => {
      const order2Page = win.open(`http://localhost:8080/checkout/${order2.bookId}`, '_blank', 'width=600,height=400');
      cy.wrap(order2Page).then((page) => {
        cy.stub(page, 'fetch')
          .callThrough()
          .withArgs(Cypress.sinon.match.has('url', `/checkout/${order2.bookId}`))
          .as('fetchOrder2');
      });
    });

    // Simulate filling order 1
    cy.get('@fetchOrder1').then(() => {
      visitAndFillOrder(order1);
    });

    // Simulate filling order 2
    cy.get('@fetchOrder2').then(() => {
      visitAndFillOrder(order2);
    });

    // Simulate submitting both orders almost simultaneously
    cy.get('@fetchOrder1').then(() => {
      submitOrder();
    });

    cy.get('@fetchOrder2').then(() => {
      submitOrder();
    });

    // Verify the order results for both users
    cy.contains('Order Approved', { timeout: 20000 }).should('be.visible');
  });
});
