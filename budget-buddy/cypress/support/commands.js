// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
Cypress.Commands.add('login', (email, password) => {
    cy.visit('/accounts/login');
    cy.get('input[name = "username"]').type(email);
    cy.get('input[name = "password"]').type(password);
    cy.get('form').submit();
});

Cypress.Commands.add('register', (url, first_name, last_name, email, password) => {
    cy.visit(url);
    cy.get('form');
    cy.get('input[name = "first_name"]').type(first_name);
    cy.get('input[name = "last_name"]').type(last_name);
    cy.get('input[name = "email"]').type(email);
    cy.get('input[name = "password1"]').type(password);
    cy.get('input[name = "password2"]').type(password);
    cy.contains('Register').click();
    //after clicking should redirect to homepage
    cy.url().should('include', '/');
});

//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })
