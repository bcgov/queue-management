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
        UsernameInput { $('input[id = "login-username"]') }
        PasswordInput { $('input[id = "login-password"]') }
        LoginButton { $('button[id = "login-button"]') }
    }

    Boolean login(String username, String password) {
        UsernameInput.value(username)
        PasswordInput.value(password)
        LoginButton.click()
        return true
    }
}