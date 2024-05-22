describe('Multiple Mixed Orders', () => {
  const orders = [
    {
      name: 'Yaroslava',
      contact: '58180469',
      creditCardNumber: '1234567890987654',
      expirationDate: '12/26',
      cvv: '123',
      street: 'turu 7',
      city: 'tartu',
      state: 'Estonia',
      zip: '51004',
      country: 'Estonia',
      title: 'Advanced CSS and Sass',
      author: 'Alex Johnson',
      price: '12',
      quantity: '1',
      shouldPass: true
    },
    {
      name: 'Fraudulent User',
      contact: '00000000',
      creditCardNumber: '9999888877776666',
      expirationDate: '01/25',
      cvv: '000',
      street: 'Fake St 123',
      city: 'Nowhere',
      state: 'Narnia',
      zip: '00000',
      country: 'Neverland',
      title: 'Hacking 101',
      author: 'Bad Guy',
      price: '1000',
      quantity: '1',
      shouldPass: false
    },
    {
      name: 'Jane Smith',
      contact: '87654321',
      creditCardNumber: '5555666677778888',
      expirationDate: '11/24',
      cvv: '789',
      street: 'Oak Street 12',
      city: 'Parnu',
      state: 'Estonia',
      zip: '80000',
      country: 'Estonia',
      title: 'Eloquent JavaScript',
      author: 'Marijn Haverbeke',
      price: '25',
      quantity: '1',
      shouldPass: true
    }
  ];

  orders.forEach(order => {
    it(`should ${order.shouldPass ? 'approve' : 'reject'} the order for ${order.name}`, () => {
      // Visit the order page
      cy.visit('/order-page')

      // Fill in user information
      cy.get('input[name="name"]').type(order.name)
      cy.get('input[name="contact"]').type(order.contact)

      // Fill in credit card information
      cy.get('input[name="creditCardNumber"]').type(order.creditCardNumber)
      cy.get('input[name="expirationDate"]').type(order.expirationDate)
      cy.get('input[name="cvv"]').type(order.cvv)

      // Fill in address information
      cy.get('input[name="street"]').type(order.street)
      cy.get('input[name="city"]').type(order.city)
      cy.get('input[name="state"]').type(order.state)
      cy.get('input[name="zip"]').type(order.zip)
      cy.get('input[name="country"]').type(order.country)

      // Fill in book details
      cy.get('input[name="title"]').type(order.title)
      cy.get('input[name="author"]').type(order.author)
      cy.get('input[name="price"]').type(order.price)
      cy.get('input[name="quantity"]').type(order.quantity)

      // Submit the order
      cy.get('button[type="submit"]').click()

      // Verify order result
      if (order.shouldPass) {
        cy.contains('Order Approved').should('be.visible')
      } else {
        cy.contains('Order Rejected').should('be.visible')
      }
    });
  });
});
