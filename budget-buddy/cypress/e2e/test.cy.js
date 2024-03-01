var stud_firstname = 'Student FN';
var stud_lastname = 'Student LN';
var stud_email =
    'student_' +
    Math.random()
        .toString(36)
        .replace(/[^a-z]+/g, '')
        .substr(0, 9) +
    '@email.com';
var stud_password = (Math.random().toString(36) + '00000000000000000').slice(2, 12);

var teach_firstname = 'Teacher FN';
var teach_lastname = 'Teacher LN';
var teach_email =
    'teacher_' +
    Math.random()
        .toString(36)
        .replace(/[^a-z]+/g, '')
        .substr(0, 9) +
    '@email.com';
var teach_password = (Math.random().toString(36) + '00000000000000000').slice(2, 12);

describe('Register student', () => {
    it('Test register form', () => {
        cy.register('/accounts/', stud_firstname, stud_lastname, stud_email, stud_password);
    });
});

describe('Register teacher', () => {
    it('Test Register Form', () => {
        cy.register('/accounts/', teach_firstname, teach_lastname, teach_email, teach_password);
    });
});

describe('Student Login', () => {
    it('Test Login Form', () => {
        cy.login(stud_email, stud_password);
    });
});

describe('Teacher Login', () => {
    it('Test Login Form', () => {
        cy.login(teach_email, teach_password);
    });
});

describe('Student: Switch Role', () => {
    beforeEach(() => {
        cy.login(stud_email, stud_password);
    });
    it('Change role', () => {
        cy.visit('/accounts/profile/update/');
        cy.get('select').eq(1).select('Student').should('have.value', '1');
        cy.get('form').submit();
    });
});

describe('Teacher: Switch Role', () => {
    beforeEach(() => {
        cy.login(teach_email, teach_password);
    });
    it('Change role', () => {
        cy.visit('/accounts/profile/update/');
        cy.get('select').eq(1).select('Teacher').should('have.value', '2');
        cy.get('form').submit();
    });
});

describe('Teacher: Create Questions', () => {
    beforeEach(() => {
        cy.login(teach_email, teach_password);
    });
    it('Test Create Question Button', () => {
        cy.visit('/');
        cy.contains('Create Question');
    });
    it('Add: Two Questions', () => {
        cy.visit('/question/add');
        cy.get('input[name = "question_text"]').type('Sample question 1');
        cy.get('form').submit();
        cy.visit('/question/add');
        cy.get('input[name = "question_text"]').type('Sample question 2');
        cy.get('form').submit();
    });
    it('Test Add Choice Button', () => {
        cy.visit('/1');
        cy.contains('View Polling Result');
        cy.contains('Add choice').click();
    });
    it('Add: Choices for Question 1', () => {
        cy.visit('/1/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 1');
        cy.get('form').submit();
        cy.visit('/1/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 2');
        cy.get('form').submit();
        cy.visit('/1/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 3');
        cy.get('form').submit();
        cy.visit('/1/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 4');
        cy.get('form').submit();
    });
    it('Add: Choices for Question 2', () => {
        cy.visit('/2/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 1');
        cy.get('form').submit();
        cy.visit('/2/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 2');
        cy.get('form').submit();
        cy.visit('/2/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 3');
        cy.get('form').submit();
        cy.visit('/2/choice/add');
        cy.get('input[name = "choice_text"]').type('Choice 4');
        cy.get('form').submit();
    });
});

describe('Student: Make a poll', () => {
    beforeEach(() => {
        cy.login(stud_email, stud_password);
    });
    it('Available polls', () => {
        cy.visit('/');
        cy.contains('Available Polls');
        cy.contains('Sample question 1').click();
        cy.url().should('include', '/1');
    });
    it('View Choices', () => {
        cy.visit('/1');
        cy.contains('Choice 1');
        cy.contains('Choice 2');
        cy.contains('Choice 3');
        cy.contains('Choice 4');
        cy.get('input[id = "choice4"]').click();
        cy.get('form').submit();
    });
    it('View Results', () => {
        cy.visit('/1/results');
        cy.contains('Choice 1 -- 0 votes');
        cy.contains('Choice 2 -- 0 votes');
        cy.contains('Choice 3 -- 0 votes');
        cy.contains('Choice 4 -- ');
    });
});

describe('RBAC: Anonymous', () => {
    it('Available polls', () => {
        cy.visit('/');
        cy.contains('Available Polls');
    });
    it('View Choices: Should Redirect to Login Page', () => {
        cy.visit('/1');
        cy.url().should('include', '/accounts/login/?next=/');
    });
    it('View Results: Should Redirect to Login Page', () => {
        cy.visit('/1/results');
        cy.url().should('include', '/accounts/login/?next=/');
        cy.contains('Login');
    });
});

describe('RBAC: Student', () => {
    beforeEach(() => {
        cy.login(stud_email, stud_password);
    });
    it('Add Question: Should Redirect', () => {
        cy.visit('/question/add');
        cy.url().should('include', '/');
        cy.contains(stud_email);
    });
    it('Add Choice: Should Redirect', () => {
        cy.visit('/1/choice/add');
        cy.contains(stud_email);
    });
});
