describe('Single Non-Fraudulent Order', () => {
  it('should place a non-fraudulent order successfully', () => {
    // Navigate to the book details page (assuming book ID 3 for the test)
    cy.visit('http://localhost:8080/books/3')

    // Wait for the page to load and click the checkout button
    cy.contains('Checkout').click()

    // Ensure the checkout page is loaded
    cy.url().should('include', '/checkout/3')

    // Fill in user information
    cy.get('input[name="userName"]').type('Yaroslava')
    cy.get('input[name="userContact"]').type('58180469')

    // Fill in credit card information
    cy.get('input[name="creditCardNumber"]').type('4111111111111111')
    cy.get('input[name="creditCardExpirationDate"]').type('12/26')
    cy.get('input[name="creditCardCVV"]').type('123')

    // Fill in billing address
    cy.get('input[name="billingAddressStreet"]').type('turu 7')
    cy.get('input[name="billingAddressCity"]').type('tartu')
    cy.get('input[name="billingAddressState"]').type('Estonia')
    cy.get('input[name="billingAddressZip"]').type('51004')
    cy.get('select[name="billingAddressCountry"]').select('Estonia')

    // Accept terms and conditions
    cy.get('input[name="termsAndConditionsAccepted"]').check()

    // Submit the order
    cy.get('button[type="Submit"]').click()

    // Verify order approval
    cy.contains('Order Approved').should('be.visible')
  })
})
