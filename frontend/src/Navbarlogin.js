import React from 'react';
import 'bootstrap-icons/font/bootstrap-icons.css';
import logo from './wildtrack-logo.png'

const Navbar = () => {
    return ( <nav class="navbar navbar-expand-lg navbar-light" min-height="60px" height="60px" style={{'background-color':'#4E342E', 'margin-bottom': '0px'}}>
    <div class="container-fluid" >
    <a href="/">
    <img src={logo} alt="" width="230" height="60" style={{'margin-top':20}}>
      </img>
      </a>      
      </div>

  </nav>
);
}
export default Navbar