<template>
  <!-- Service Model Popup -->
  <v-dialog
    v-model="isModalOpen"
    max-width="570"
  >
    <v-card>
      <v-toolbar dark flat color="primary">
        <v-toolbar-title>Terms of Use</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon dark @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <h3 class='text-center my-4'>TERMS OF USE </h3>
        <h4 class='text-center my-4'>Version 1.0, May 19th, 2020</h4>
        <p>The "Book an Appointment" application (the <span class="bold">"Service"</span>) allows you, the user to book an appointment at a Service BC location for services offered at that location. </p>
        <p>These Terms of Use are an agreement between you and Her Majesty the Queen in Right of the Province of British Columbia, represented by the Minister of Citizens' Services, IDIM (the <span class="bold">"Province"</span>), and govern your use of the Service. By indicating that you agree to these Terms of Use, and in consideration of the use of the Service, you agree to the following:</p>

        <p class="bold">1. Authority and Ability to Accept Terms of Use</p>
        <p>In order to accept these Terms of Use and use the Service, you must: (a) have a BCeID or a BC Service Card; and (b) be at least 19 years of age.</p>

        <p class="bold">2. Responsibility for Use</p>
        <p>You are solely responsible for your use of the Service, including without limitation for taking reasonable precautions to ensure that any information that you provide in connection with your use of the Service (such as your BCeID, your BC Services Card number, and any "personal information", as that term is defined in the <span class="italic">Freedom of Information and Protection of Privacy Act</span> (B.C.)) is kept confidential.</p>

        <p class="bold">3. Ownership</p>
        <p>The Service, the website through which the Service is accessed, and all other information and works made available, displayed or transmitted in connection with the Service, including without limitation data, text, audio, video, trademarks, trade names, logos, domain names, images, graphics, graphical user interface elements and designs, in any form or medium whatsoever (collectively, the <span class="bold">"Content"</span>), are owned by the Province or its licensors and are protected by copyright, patent, trademark and other laws protecting intellectual property rights.  </p>

        <p class="bold">4. License</p>
        <p>Subject to your compliance with these Terms of Use, the Province grants you a non-exclusive, revocable, limited license to access and use the Service and the Content solely as necessary for you to book and manage your appointments.  You must not copy, distribute, republish, transmit or otherwise exploit any part of the Service or the Content, and the Province expressly reserves all intellectual property rights in and to the Service and the Content.  If your use of the Service is terminated under section 5, your license is automatically terminated.</p>

        <p class="bold">5. Suspension or Termination</p>
        <p>The Province may at any time, in its sole discretion, suspend or terminate your use of the Service, in whole or in part: (a) if you fail to comply with any provision of these Terms of Use; (b) as a security measure; or (c) for administrative purposes.</p>

        <p class="bold">6. Changes to Service and/or Terms of Use</p>
        <p>The Province may at any time, in its sole discretion and without direct notice to you: (a) discontinue the Service; or (b) make changes to the Service and/or these Terms of Use.  By continuing to use the Service, you will be conclusively deemed to have accepted any changes to these Terms of Use.</p>

        <p class="bold">7. Acceptable Use</p>
        <p>You must not take any action in connection with your use of the Service that would jeopardize the security, integrity and/or availability of the Service, including without limitation:</p>
        <ol class='mb-4' type="a">
          <li>using the Service for any unlawful or inappropriate purpose;</li>
          <li>decompiling, disassembling, reverse engineering or otherwise copying any software associated with the Service;</li>
          <li>tampering with any portion of the Service;</li>
          <li>using the Service to transmit any virus or other harmful or destructive computer code, files or programs or to conduct hacking and/or intrusion activities;</li>
          <li>attempting to circumvent or subvert any security measure associated with the Service;</li>
          <li>taking any action that might reasonably be construed as likely to adversely affect other users of the Service; or</li>
          <li>removing or altering any proprietary symbol or notice, including any copyright notice, trademark or logo, displayed in connection with the Service.</li>
        </ol>

        <p class="bold">8. Privacy</p>
        <p>When you use the Service, "personal information" (as that term is defined in the <span class="italic">Freedom of Information and Protection of Privacy Act</span> (B.C.)) that you have entered to log in with your BCeID or BC Services Card is collected by the Ministry of Citizen’s Services via the Service.  The Ministry of Citizens’ Services also collects your address in order to provide you with the nearest Service BC office location.   The authority for the collection of this information is sections 26(c), 27(1)(b), 33.1(5) and 33.2(a) of the <span class="italic">Freedom of Information and Protection of Privacy Act</span>.  Any questions that you may have about the collection of your personal information can be direct to: Director, Service Delivery, PO BOX 9412 STN PROV GOVT, Victoria, BC, V8W 9V1, 1 800 663-7867</p>

        <p class="bold">9. Service Provided "As Is"</p>
        <p>The Service is provided to you “as is”, and the Province disclaims all representations, warranties, conditions, obligations and liabilities of any kind, whether express or implied, in relation to the Service, including without limitation implied warranties with respect to merchantability, satisfactory quality, fitness for a particular purpose and non-infringement.  Without limiting the general nature of the previous sentence, the Province does not represent or warrant that:</p>
        <ol class='mb-4' type="a">
          <li>the Service will be available;</li>
          <li>your use of the Service will be timely, uninterrupted or error free;</li>
          <li>any errors in the Service will be corrected; or</li>
          <li>the Service will meet your expectations and requirements.</li>
        </ol>

        <p class="bold">10. No Liability</p>
        <p>To the maximum extent permitted by applicable law, under no circumstances will the Province be liable to any person or entity for any direct, indirect, special, incidental, consequential or other loss, claim, injury or damage, whether foreseeable or unforeseeable (including without limitation claims for damages for loss of profits or business opportunities, use or misuse of, or inability to use, the Service, interruptions, deletion or corruption of files, loss of programs or information, errors, defects or delays) arising out of or in any way connected with your use of the Service and whether based on contract, tort, strict liability or any other legal theory.  The previous sentence will apply even if the Province has been specifically advised of the possibility of any such loss, claim, injury or damage.</p>

        <p class="bold">11. Indemnity</p>
        <p>You agree to indemnify, defend and hold harmless the Province and the Province’s employees and agents from and against all claims, demands, obligations, losses, liabilities, costs or debts, and expenses (including but not limited to reasonable legal fees) arising from:  (a) your use of the Service; or (b) your violation of any provision of these Terms of Use.</p>

        <p class="bold">12. General</p>
        <p>These Terms of Use are the entire agreement between you and the Province with respect to the subject matter of these Terms of Use. The headings in these Terms of Use are inserted for convenience only, and will not be used in interpreting or construing any provision of these Terms of Use.  If any provision of these Terms of Use is invalid, illegal or unenforceable, that provision will be severed from these Terms of Use and all other provisions will remain in full force and effect.  These Terms of Use will be governed by and construed in accordance with the laws of the province of British Columbia and the applicable laws of Canada.  By using the Service, you consent to the exclusive jurisdiction and venue of the courts of the province of British Columbia, sitting in Victoria, for the hearing of any dispute arising from or related to these Terms of Use and their subject matter.</p>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class TermsOfServicePopup extends Vue {
  // @Prop({ default: false })
  // private isModalOpen!: boolean
  private isModalOpen: boolean = false

  public open () {
    this.isModalOpen = true
  }

  public close () {
    this.isModalOpen = false
  }
}
</script>

<style lang="scss" scoped>
// @import "@/assets/scss/theme.scss";

.bold {
  font-weight: bold
}
.italic {
  font-style: italic;
}
</style>
