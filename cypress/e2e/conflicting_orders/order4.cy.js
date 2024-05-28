describe('Conflicting Order 2', () => {
    const order = {
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
  
    it('should place an order for User 2', () => {
      cy.visit(`http://localhost:8080/books/${order.bookId}`);
      cy.contains('Checkout').click();
      
      cy.url().should('include', `/checkout/${order.bookId}`);
      
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
      
      cy.get('button[type="submit"]').click();
      
      cy.contains('Order Approved', { timeout: 50000 }).should('be.visible');
    });
  });
  