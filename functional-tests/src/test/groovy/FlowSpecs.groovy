import geb.spock.GebReportingSpec

import pages.MainPage

import spock.lang.Unroll
import spock.lang.Title

@Title("Ensure app is accessible")
class FlowSpecs extends GebReportingSpec {

    @Unroll
    def "Ensure page loads" () {
        given: "I navigate to the App"
            to MainPage
        then: "Login button is present"
            LoginButton
    }

    @Unroll
    def "Perform login" () {
        given: "I navigate to the App"
            to MainPage
        when: "I fill in and submit the form"
            MainPage.UsernameInput.value("vancouver1")
            MainPage.PasswordInput.value("vancouver1")
            MainPage.LoginButton.click()
        then: "Login form is no longer present"
            !LoginButton.displayed
    }
}