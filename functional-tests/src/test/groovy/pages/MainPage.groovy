package pages
import geb.Page
import modules.LoginModule

class MainPage extends Page {
    static at = { title == "Queue Management Proof of Concept" }
    static content = {
    	loginModule { module LoginModule } 
    }
}
