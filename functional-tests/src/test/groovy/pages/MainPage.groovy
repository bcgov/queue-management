package pages
import geb.Page

class MainPage extends Page {
    static at = { title == "Queue Management Proof of Concept" }
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
