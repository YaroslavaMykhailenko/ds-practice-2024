describe('Multiple Non-Fraudulent Non-Conflicting Orders', () => {
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
      quantity: '1'
    },
    {
      name: 'John Doe',
      contact: '12345678',
      creditCardNumber: '1111222233334444',
      expirationDate: '01/25',
      cvv: '456',
      street: 'Main St 1',
      city: 'Tallinn',
      state: 'Estonia',
      zip: '10111',
      country: 'Estonia',
      title: 'JavaScript: The Good Parts',
      author: 'Douglas Crockford',
      price: '20',
      quantity: '2'
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
      quantity: '1'
    }
  ];

  orders.forEach((order, index) => {
    it(`should place an order for ${order.name} successfully`, () => {
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

      // Verify order approval
      cy.contains('Order Approved').should('be.visible')
    });
  });
});
