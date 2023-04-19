/* eslint-disable import/no-anonymous-default-export */
/* eslint-disable no-console */
/* eslint-disable no-undef */
import 'bootstrap-icons/font/bootstrap-icons.css';
import React from 'react'
import { useNavigate } from 'react-router-dom'


export default function () {
  const navigate = useNavigate()
  const queryParams = new URLSearchParams(window.location.search)

  function login (){
const myHeaders = new Headers();
myHeaders.append('Authorization', `Bearer ${  token}`);
const raw = '';
const requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};
fetch('https://rtvb5hreoe.execute-api.us-east-1.amazonaws.com/dev/_api/v1/user/new', requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
  }

  const myHeaders = new Headers();
  myHeaders.append('content-type', 'application/x-www-form-urlencoded');
  myHeaders.append('authorization', 'Basic NGZxMTU4dWRocmptOTRlazk4dTRhOWZoaTI6MXFjOThpdDk2b3RqZnFzNjZzbXE5MDV2NGI3OTNhMnBmcTNrZ3U3NDg4a2trbWdxNDE0MQ==');

  const urlencoded = new URLSearchParams();
  urlencoded.append('grant_type', 'authorization_code');
  urlencoded.append('client_id', '4fq158udhrjm94ek98u4a9fhi2');
  urlencoded.append('code', queryParams.get('code'));
  urlencoded.append('redirect_uri', 'https://d11qqejcjwv6a0.cloudfront.net/media-upload');
let token;
  const requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: urlencoded,
    redirect: 'follow'
  };

  fetch('https://wildtrack-auth.auth.us-east-1.amazoncognito.com/oauth2/token', requestOptions)
    .then(response => response.json())
    .then(result => {
    token = result.access_token
    console.log(token)
     console.log(typeof result)
    sessionStorage.setItem('token',result.access_token)
    console.log('loginResponse', `sessionStorage set with token value: ${result.access_token}`)
   
    if(sessionStorage.getItem('token') === undefined) {
      navigate('/')
      alert('Login Failed')
    } else{
      login ();
      
      navigate('/profile')
    
    }
  }
    )
    .catch(error => console.log('error', error));  
  
    return (
      <div className="App">
        
      </div>
  )


}