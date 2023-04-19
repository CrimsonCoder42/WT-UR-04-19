/* eslint-disable no-console */
// import fetch from 'node-fetch';
/* eslint-disable no-undef */
import 'bootstrap-icons/font/bootstrap-icons.css';
import React from 'react';
import { useNavigate } from 'react-router-dom'
import wildtracklogo from './watermark.png'

const Navbar = () => {
  const navigate = useNavigate()
  function logout() {
    const urlencoded = new URLSearchParams({
      response_type: 'code',
      client_id: '4fq158udhrjm94ek98u4a9fhi2',
      redirect_uri: 'https://d3crdvaffca4ns.cloudfront.net'
    })
    
    fetch(`https://wildtrack-auth.auth.us-east-1.amazoncognito.com/logout?${  urlencoded}`, {
      method: 'GET',
      crossorigin: true,
      mode: 'no-cors'
    })
    .catch((error) => {
      console.log(error)
    })

    sessionStorage.removeItem('token')

    navigate('/')
  }
    return ( 
      <nav class="navbar navbar-expand-lg navbar-light" min-height="60px" height="60px" style={{'background-color':'#4E342E', 'margin-bottom': '0px', 'display':'flex', 'flex-direction': 'row','flex-wrap': 'nowrap', 'justify-content': 'space-between', 'align-items': 'center', 'flex-flow':'row nowrap', }}>
    <div class="container-fluid" style={{'display':'flex', 'justify-content':'space-between','flex-direction':'row','align-items':'center','width':'100%'}}>
      <div style={{'width':'50%','display':'flex','float':'left'}}>
    <a href="/">
    <img class="logo" src={wildtracklogo} alt="Wildtrack logo" >
      </img>
      </a>
      </div>
      <div style={{'display':'flex','width':'50%','float':'right','flex-direction':'row-reverse'}}>
      <button onClick={logout} type="button" >
          <span  style={{'text-align':'right'}}class="glyphicon glyphicon-log-out"></span> Log out
        </button>   
        </div>   
      </div>

  </nav>
   
);
}
export default Navbar