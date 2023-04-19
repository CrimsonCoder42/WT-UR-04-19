/* eslint-disable no-unused-vars */
/* eslint-disable prefer-arrow-callback */
/* eslint-disable no-console */
/* eslint-disable import/no-anonymous-default-export */
import 'bootstrap-icons/font/bootstrap-icons.css';

import React, { useState } from 'react'
import logos from './backgrounding.jpg'
import PrivacyPolicy from './Privacy.pdf'
import watermarks from './watermark.png'



export default function () {
  const[agreedToPolicy, setAgreedToPolicy] = useState(false);
  const [closedModal, setClosedModal] = useState(false);
  const [agreedPdf, setAgreedPdf] = useState(false);
function cancelPDF (){
  setAgreedToPolicy(false);
  const checkbox = document.getElementById('agree')
  checkbox.checked = false;
}
function agreedToPdf (){
  setAgreedToPolicy(false);
  setAgreedPdf(true);
  setClosedModal(true)
  
}
  function PrivacyPolicyPopup(props) {
  function jump (){
      // eslint-disable-next-line no-var
      var iframe = document.getElementById('heighting');
      iframe.addEventListener('load', function() {
        iframe.contentWindow.scrollTo(0, iframe.contentWindow.document.body.scrollHeight);
      });     
       console.log(iframe)
    }
    const privacyPolicyIframe = document.getElementById('privacy-policy-iframe');
    const acceptButton = document.getElementById('accept-button');
 /*  privacyPolicyIframe.addEventListener('load', function() {
      const iframeDocument = privacyPolicyIframe.contentDocument || privacyPolicyIframe.contentWindow.document;
      const iframeBody = iframeDocument.body;
    
      iframeBody.addEventListener('scroll', function() {
        if (iframeBody.scrollTop + iframeBody.clientHeight >= iframeBody.scrollHeight) {
          acceptButton.disabled = false;
        }
      });
    })*/;
  
    return (
        <div id='modal'>
          <div id='modal-content'> 
        <div id="modal-text">
        <iframe id="heighting" src={PrivacyPolicy} title="Privacy Policy" ></iframe>
        <button id="cancel" onClick={cancelPDF} onclick="parent.document.getElementById('heighting').style.display = 'none'">X</button>
        </div>
        <button onClick={jump}>Jump to Bottom</button>
        <button onClick={agreedToPdf}>Accept</button>
      </div>
      </div>

    );
  }
  const handleAgree = (event) =>{
    setAgreedToPolicy(event.target.checked);
    if(!event.target.checked){
      setAgreedToPolicy(false);
      setClosedModal(false)

    } else {
      setAgreedToPolicy(true);
      handlePrivacyPolicyAgree();
    }
  }
  const handlePrivacyPolicyAgree = () => {
   // setShowPrivacyPolicy(true);
  }
  const handledclick = (event) => {
    if(!agreedToPolicy){
      event.preventDefault();
      alert('To sign up, please review the privacy policy and agree')
    }
  }
    return (
        <div >
              <div className="Auth-form-container" style={{backgroundImage: `url(${logos})`, 'background-repeat':'no-repeat', 'background-size': 'cover', 'display': 'flex', 'justify-content':'center','align-items':'stretch','width': '100vw','height':'100vh','flex-direction':'row','flex-wrap':'wrap', 'align-content':'flex-start' }}>
                <div class="picture" style={{'display' :'block', 'textAlign':'center', 'margin-top':'30px', 'margin-bottom':'20px','horizontal-align':'center'}}>
              <img src={watermarks} alt= "Wildtrack logo"  />
              </div>
        <div class="box-container" style={{}}>
        <form className="Auth-form"  >
          <div className="Auth-form-content" >
            <h1 className="Auth-form-title" style={{color: '#348e47', }}>Log In to WildTrack!</h1>
            
            
            <p className="forgotpassword" style={{'color':'#4E342E' }}>
          
            <a href="https://wildtrack-auth.auth.us-east-1.amazoncognito.com/forgotPassword?client_id=4fq158udhrjm94ek98u4a9fhi2&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fd11qqejcjwv6a0.cloudfront.net%2Fmedia-upload" style={{'color':'#4E342E'}}><b> Forgot your password?</b></a>
            </p>

 
            <div className="d-grid gap-2 mt-3" style={{'text-align': 'center', 'margin-bottom': '20px'}}>
              <button style={{ 'background-color':'#348e47','border':'2px solid white', 'padding-top':'5px','padding-bottom':'5px', 'padding-left': '30px',  'padding-right': '30px', 'border-radius': '0px'}} type="button" className="btn btn-primary">
                <a style={{'text-decoration-line': 'none', 'color': 'white'}}href="https://wildtrack-auth.auth.us-east-1.amazoncognito.com/login?client_id=4fq158udhrjm94ek98u4a9fhi2&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fd11qqejcjwv6a0.cloudfront.net%2Fmedia-upload"><b>Log In</b></a>
              </button>
            </div>


          </div>
        </form>
        <div className="signup-container" >
        <h1 class="noaccount" ><b>No account yet?</b></h1>
        <h4 class="signupbelow">Sign up for an account below.</h4>


        <div className="form-group mt-3" style={{ 'display':'inline-flex', 'padding-left': '10px'}}>
          <input onChange={handleAgree} style={{'text-align': 'center'}}
              type="checkbox"
              className="form-control mt-1"
              id="agree"
              required
              on
            />
            
            <label required style={{'color':'white'}}><a style={{'text-decoration':'underline','color':'white'}}href={PrivacyPolicy} target= "_blank" rel="noreferrer">Privacy Notice</a> - I agree to the terms and conditions</label>
            
          </div>
          <div>
            {!agreedToPolicy ? (<div></div>): <div><PrivacyPolicyPopup/> </div>}
          </div>
          <div className="form-group mt-3" style={{ 'display':'inline-flex', 'padding-left': '10px'}}>
          <input onChange= {handleAgree} style={{'text-align': 'center'}}
              type="checkbox"
              className="form-control mt-1"
              id="agree2"
              required
              on
            />
             <label style={{'color':'white'}}>Send me the WildTrack newsletter</label>
          </div>
          <div id="button">
          <button id ="actualbutton"  disabled={!closedModal}  className="link-primary"  >
  <a id="links" roled="link"  onClick={handledclick} style={{'color': '#348e47', 'border-radius':'0px'}}href="https://wildtrack-auth.auth.us-east-1.amazoncognito.com/signup?client_id=4fq158udhrjm94ek98u4a9fhi2&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fd11qqejcjwv6a0.cloudfront.net%2Fmedia-upload"><b>Sign Up</b></a>
</button>
          </div>
          </div>

              </div>
      </div>
      </div>
 
    )
  }

