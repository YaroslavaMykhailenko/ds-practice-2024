describe('Multiple Mixed Orders', () => {
  const orders = [
    {
      name: 'Yaroslava',
      contact: '58180469',
      creditCardNumber: '4111111111111111',
      expirationDate: '12/26',
      cvv: '123',
      street: 'turu 7',
      city: 'tartu',
      state: 'Estonia',
      zip: '51004',
      country: 'Estonia',
      bookId: 3,
      shouldPass: true
    },
    {
      name: 'Fraudulent User',
      contact: '00000000',
      creditCardNumber: '9999888877776666',
      expirationDate: '01/20',
      cvv: '000',
      street: 'Fake St 123',
      city: 'Nowhere',
      state: 'Narnia',
      zip: '00000',
      country: 'Finland',
      bookId: 4,
      shouldPass: false
    },
    {
      name: 'Jane Smith',
      contact: '87654321',
      creditCardNumber: '4111111111111111',
      expirationDate: '11/24',
      cvv: '789',
      street: 'Oak Street 12',
      city: 'Parnu',
      state: 'Estonia',
      zip: '80000',
      country: 'Estonia',
      bookId: 5,
      shouldPass: true
    }
  ];

  orders.forEach(order => {
    it(`should ${order.shouldPass ? 'approve' : 'reject'} the order for ${order.name}`, () => {
      // Visit the book details page
      cy.visit(`http://localhost:8080/books/${order.bookId}`)

      // Wait for the page to load and click the checkout button
      cy.contains('Checkout').click()

      // Ensure the checkout page is loaded
      cy.url().should('include', `/checkout/${order.bookId}`)

      // Fill in user information
      cy.get('input[name="userName"]').type(order.name)
      cy.get('input[name="userContact"]').type(order.contact)

      // Fill in credit card information
      cy.get('input[name="creditCardNumber"]').type(order.creditCardNumber)
      cy.get('input[name="creditCardExpirationDate"]').type(order.expirationDate)
      cy.get('input[name="creditCardCVV"]').type(order.cvv)

      // Fill in billing address
      cy.get('input[name="billingAddressStreet"]').type(order.street)
      cy.get('input[name="billingAddressCity"]').type(order.city)
      cy.get('input[name="billingAddressState"]').type(order.state)
      cy.get('input[name="billingAddressZip"]').type(order.zip)
      cy.get('select[name="billingAddressCountry"]').select(order.country)

      // Accept terms and conditions
      cy.get('input[name="termsAndConditionsAccepted"]').check()

      // Submit the order
      cy.get('button[type="submit"]').click()

      // Verify order result
      if (order.shouldPass) {
        cy.url({ timeout: 250000 }).should('include', `/checkout/${order.bookId}/confirmation`)
        cy.contains('Order Approved', { timeout: 250000 }).should('be.visible')
      } else {
        cy.contains('Order Rejected', { timeout: 250000 }).should('be.visible')
      }
    });
  });
});
