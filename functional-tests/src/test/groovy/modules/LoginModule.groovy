package modules

import geb.Module
import geb.Browser
import pages.MainPage
import geb.spock.GebReportingSpec
import spock.lang.Unroll

/**
 * Example of a Module in Groovy.
 */

class LoginModule extends Module {

    static content = {
        usernameInput { $('input', id: "login-username") }
        passwordInput { $('input', id: "login-password") }
        loginButton { $('button', id: "login-button") }
        logoutButton { $('button', id: "logout-button") }
    }

    void login(String username, String password) {
        usernameInput.value(username)
        passwordInput.value(password)
        loginButton.click()
    }
}