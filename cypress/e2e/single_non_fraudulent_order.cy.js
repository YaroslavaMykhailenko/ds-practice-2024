describe('Single Non-Fraudulent Order', () => {
  it('should place a non-fraudulent order successfully', () => {
    // Visit the order page
    cy.visit('/order-page')

    // Fill in user information
    cy.get('input[name="name"]').type('Yaroslava')
    cy.get('input[name="contact"]').type('58180469')

    // Fill in credit card information
    cy.get('input[name="creditCardNumber"]').type('1234567890987654')
    cy.get('input[name="expirationDate"]').type('12/26')
    cy.get('input[name="cvv"]').type('123')

    // Fill in address information
    cy.get('input[name="street"]').type('turu 7')
    cy.get('input[name="city"]').type('tartu')
    cy.get('input[name="state"]').type('Estonia')
    cy.get('input[name="zip"]').type('51004')
    cy.get('input[name="country"]').type('Estonia')

    // Fill in book details
    cy.get('input[name="title"]').type('Advanced CSS and Sass')
    cy.get('input[name="author"]').type('Alex Johnson')
    cy.get('input[name="price"]').type('12')
    cy.get('input[name="quantity"]').type('1')

    // Submit the order
    cy.get('button[type="submit"]').click()

    // Verify order approval
    cy.contains('Order Approved').should('be.visible')
  })
})
