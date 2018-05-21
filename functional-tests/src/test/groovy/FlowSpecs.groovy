import geb.spock.GebReportingSpec

import pages.MainPage
import modules.LoginModule

import spock.lang.Unroll
import spock.lang.Title

@Title("Ensure app is accessible")
class FlowSpecs extends GebReportingSpec {

    @Unroll
    def "Perform login" () {
        given: "I navigate to the App"
            to MainPage
        when: "I fill in and submit the form"
            loginModule.login("vancouver1", "vancouver1")
        then: "Login form is no longer present"
            loginModule.logoutButton.present
    }
}