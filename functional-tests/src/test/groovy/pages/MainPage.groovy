package pages
import geb.Page

class MainPage extends Page {
    static at = { title == "Queue Management Proof of Concept" }
    static content = {
        
    }

    Boolean login(String username, String password) {
        UsernameInput.value(username)
        PasswordInput.value(password)
        LoginButton.click()
        return true
    }
}
