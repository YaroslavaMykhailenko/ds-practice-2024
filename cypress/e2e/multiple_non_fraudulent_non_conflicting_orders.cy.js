describe('Multiple Non-Fraudulent Non-Conflicting Orders', () => {
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
      bookId: 3
    },
    {
      name: 'John Doe',
      contact: '12345678',
      creditCardNumber: '4111111111111111',
      expirationDate: '01/25',
      cvv: '456',
      street: 'Main St 1',
      city: 'Tallinn',
      state: 'Estonia',
      zip: '10111',
      country: 'Estonia',
      bookId: 4
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
      bookId: 5
    }
  ];

  orders.forEach((order) => {
    it(`should place an order for ${order.name} successfully`, () => {
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

      // Wait for redirection to confirmation page
      cy.url({ timeout: 250000 }).should('include', `/checkout/${order.bookId}/confirmation`)

      // Verify order approval
      cy.contains('Order Approved', { timeout: 250000 }).should('be.visible')
    });
  });
});
