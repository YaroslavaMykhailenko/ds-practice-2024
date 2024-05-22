// describe('Conflicting Orders', () => {
//   const order1 = {
//     name: 'User 1',
//     contact: '11111111',
//     creditCardNumber: '1234567890987654',
//     expirationDate: '12/26',
//     cvv: '123',
//     street: 'Street 1',
//     city: 'City 1',
//     state: 'State 1',
//     zip: '11111',
//     country: 'Country 1',
//     title: 'Concurrent Book',
//     author: 'Author 1',
//     price: '15',
//     quantity: '1'
//   };

//   const order2 = {
//     name: 'User 2',
//     contact: '22222222',
//     creditCardNumber: '9876543210123456',
//     expirationDate: '11/25',
//     cvv: '456',
//     street: 'Street 2',
//     city: 'City 2',
//     state: 'State 2',
//     zip: '22222',
//     country: 'Country 2',
//     title: 'Concurrent Book',
//     author: 'Author 1',
//     price: '15',
//     quantity: '1'
//   };

//   it('should place an order for User 1 successfully', () => {
//     // Visit the order page
//     cy.visit('/order-page')

//     // Fill in user information
//     cy.get('input[name="name"]').type(order1.name)
//     cy.get('input[name="contact"]').type(order1.contact)

//     // Fill in credit card information
//     cy.get('input[name="creditCardNumber"]').type(order1.creditCardNumber)
//     cy.get('input[name="expirationDate"]').type(order1.expirationDate)
//     cy.get('input[name="cvv"]').type(order1.cvv)

//     // Fill in address information
//     cy.get('input[name="street"]').type(order1.street)
//     cy.get('input[name="city"]').type(order1.city)
//     cy.get('input[name="state"]').type(order1.state)
//     cy.get('input[name="zip"]').type(order1.zip)
//     cy.get('input[name="country"]').type(order1.country)

//     // Fill in book details
//     cy.get('input[name="title"]').type(order1.title)
//     cy.get('input[name="author"]').type(order1.author)
//     cy.get('input[name="price"]').type(order1.price)
//     cy.get('input[name="quantity"]').type(order1.quantity)

//     // Submit the order
//     cy.get('button[type="submit"]').click()

//     // Verify order approval
//     cy.contains('Order Approved').should('be.visible')
//   });

//   it('should place an order for User 2 successfully', () => {
//     // Visit the order page
//     cy.visit('/order-page')

//     // Fill in user information
//     cy.get('input[name="name"]').type(order2.name)
//     cy.get('input[name="contact"]').type(order2.contact)

//     // Fill in credit card information
//     cy.get('input[name="creditCardNumber"]').type(order2.creditCardNumber)
//     cy.get('input[name="expirationDate"]').type(order2.expirationDate)
//     cy.get('input[name="cvv"]').type(order2.cvv)

//     // Fill in address information
//     cy.get('input[name="street"]').type(order2.street)
//     cy.get('input[name="city"]').type(order2.city)
//     cy.get('input[name="state"]').type(order2.state)
//     cy.get('input[name="zip"]').type(order2.zip)
//     cy.get('input[name="country"]').type(order2.country)

//     // Fill in book details
//     cy.get('input[name="title"]').type(order2.title)
//     cy.get('input[name="author"]').type(order2.author)
//     cy.get('input[name="price"]').type(order2.price)
//     cy.get('input[name="quantity"]').type(order2.quantity)

//     // Submit the order
//     cy.get('button[type="submit"]').click()

//     // Verify order approval
//     cy.contains('Order Approved').should('be.visible')
//   });
// });


describe('Conflicting Orders', () => {
  const order1 = {
    name: 'User 1',
    contact: '11111111',
    creditCardNumber: '1234567890987654',
    expirationDate: '12/26',
    cvv: '123',
    street: 'Street 1',
    city: 'City 1',
    state: 'State 1',
    zip: '11111',
    country: 'Country 1',
    title: 'Concurrent Book',
    author: 'Author 1',
    price: '15',
    quantity: '1'
  };

  const order2 = {
    name: 'User 2',
    contact: '22222222',
    creditCardNumber: '9876543210123456',
    expirationDate: '11/25',
    cvv: '456',
    street: 'Street 2',
    city: 'City 2',
    state: 'State 2',
    zip: '22222',
    country: 'Country 2',
    title: 'Concurrent Book',
    author: 'Author 1',
    price: '15',
    quantity: '1'
  };

  it('should handle conflicting orders for the same book', () => {
    cy.visit('/order-page')

    // User 1 places order
    cy.window().then(win => {
      const win1 = win.open('/order-page', '_blank', 'width=600,height=400');
      win1.onload = () => {
        win1.document.querySelector('input[name="name"]').value = order1.name;
        win1.document.querySelector('input[name="contact"]').value = order1.contact;
        win1.document.querySelector('input[name="creditCardNumber"]').value = order1.creditCardNumber;
        win1.document.querySelector('input[name="expirationDate"]').value = order1.expirationDate;
        win1.document.querySelector('input[name="cvv"]').value = order1.cvv;
        win1.document.querySelector('input[name="street"]').value = order1.street;
        win1.document.querySelector('input[name="city"]').value = order1.city;
        win1.document.querySelector('input[name="state"]').value = order1.state;
        win1.document.querySelector('input[name="zip"]').value = order1.zip;
        win1.document.querySelector('input[name="country"]').value = order1.country;
        win1.document.querySelector('input[name="title"]').value = order1.title;
        win1.document.querySelector('input[name="author"]').value = order1.author;
        win1.document.querySelector('input[name="price"]').value = order1.price;
        win1.document.querySelector('input[name="quantity"]').value = order1.quantity;
        win1.document.querySelector('button[type="submit"]').click();
      };
    });

    // User 2 places order
    cy.window().then(win => {
      const win2 = win.open('/order-page', '_blank', 'width=600,height=400');
      win2.onload = () => {
        win2.document.querySelector('input[name="name"]').value = order2.name;
        win2.document.querySelector('input[name="contact"]').value = order2.contact;
        win2.document.querySelector('input[name="creditCardNumber"]').value = order2.creditCardNumber;
        win2.document.querySelector('input[name="expirationDate"]').value = order2.expirationDate;
        win2.document.querySelector('input[name="cvv"]').value = order2.cvv;
        win2.document.querySelector('input[name="street"]').value = order2.street;
        win2.document.querySelector('input[name="city"]').value = order2.city;
        win2.document.querySelector('input[name="state"]').value = order2.state;
        win2.document.querySelector('input[name="zip"]').value = order2.zip;
        win2.document.querySelector('input[name="country"]').value = order2.country;
        win2.document.querySelector('input[name="title"]').value = order2.title;
        win2.document.querySelector('input[name="author"]').value = order2.author;
        win2.document.querySelector('input[name="price"]').value = order2.price;
        win2.document.querySelector('input[name="quantity"]').value = order2.quantity;
        win2.document.querySelector('button[type="submit"]').click();
      };
    });

    // Verify order result
    cy.contains('Order Approved').should('be.visible');
  });
});
