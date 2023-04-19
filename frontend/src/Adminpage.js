/* eslint-disable one-var */
/* eslint-disable no-var */
/* eslint-disable no-lonely-if */
/* eslint-disable eqeqeq */
/* eslint-disable prefer-const */
/* eslint-disable no-console */
/* eslint-disable no-else-return */
/* eslint-disable no-unused-vars */
/* eslint-disable import/no-anonymous-default-export */

import { FaPencilAlt, FaTrash, FaBan} from 'react-icons/fa';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faArrowRight } from '@fortawesome/free-solid-svg-icons';
import '@fortawesome/fontawesome-free/css/all.css';



import ReactPaginate from 'react-paginate';

import React, { useState }  from 'react';
import Navbar from './Navbarloggedin';

export default function ()  {
    const tableData = [
        { id: 1, 'First Name': 'Alice', 'Last Name': 25, email: 'alice@example.com', 'organization':'San Diego Zoo', numofobs: 1, lastActive: '2/21/2023', createdOn: '1/2/2023', status: 'Verified', userRole: 'Contributor'},
        { id: 2, 'First Name': 'Bob', 'Last Name': 30, email: 'bob@example.com', 'organization':'San Diego Zoo' , numofobs: 1 , lastActive: '2/21/2023', createdOn: '1/2/2023',status: 'Invited', userRole: 'Contributor'},
        { id: 3, 'First Name': 'Charlie', 'Last Name': 35, email: 'charlie@example.com', 'organization':'San Diego Zoo', numofobs: 1, lastActive: '2/20/2023',createdOn: '1/3/2023', status: 'Verified', userRole: 'Contributor'  }, { id: 4, 'First Name': 'Charlie', 'Last Name': 35, email: 'charlie@example.com', 'organization':'San Diego Zoo', numofobs: 1, lastActive: '2/21/2023',createdOn: '1/2/2023', status: 'Pending', userRole: 'Contributor'  },
        { id: 5, 'First Name': 'Charlie', 'Last Name': 35, email: 'charlie@example.com', 'organization':'San Diego Zoo', numofobs: 1, lastActive: '2/21/2023',createdOn: '1/2/2023', status: 'Banned', userRole: 'Contributor'  }, { id: 6, 'First Name': 'Charlie', 'Last Name': 35, email: 'charlie@example.com', 'organization':'San Diego Zoo', numofobs: 1, lastActive: '2/21/2023',createdOn: '1/2/2023', status: 'Unverified', userRole: 'Contributor'  },
        
      ];
 const columns = [
  {Header: 'ID', accessor: 'id'},
  {Header: 'First Name', accessor: 'firstname'},
  {Header: 'Last Name', accessor: 'lastname'},
  {Header:'Email', accessor: 'email'},
  {Header: 'Organization', accessor: 'organization'},
  {Header:'# Submitted Observations', accessor: 'submitted'},
  {Header: 'Last Active', accessor: 'lastactive'},
  {Header: 'Created On', accessor: 'created'},
  {Header: 'Status', accessor: 'status'},
  {Header: 'User Role', accessor: 'userrole'},
]
const [selectedOption, setSelectedOption] = useState('');

const handleSelectChange = (event) => {
        setSelectedOption(event.target.value);
      }
const [searchQuery, setSearchQuery] = useState('');
const [showSearchList, setShowSearchList] = useState(false);
const handleSearchButtonClick = () => {
      setShowSearchList(!showSearchList);
    };
const [currentPage, setCurrentPage] = useState(0);
const itemsPerPage = 5; // change this to the number of items you want to display per page
const handlePageChange = ({ selected }) => {
  setCurrentPage(selected);
};
const pageCount = Math.ceil(tableData.length / itemsPerPage);
const offset = currentPage * itemsPerPage;
const filteredData = tableData.filter((item) =>
  item['First Name'].toLowerCase().includes(searchQuery.toLowerCase())
);
const currentPageItems = filteredData.slice(offset, offset + itemsPerPage);
// eslint-disable-next-line consistent-return
const getStatusColor = (status) => {
  if (status === 'Verified') {
       return { backgroundColor: 'green', borderRadius: '95%', color: 'white' };
  } else if (status === 'Banned') {
    return { backgroundColor: 'red', borderRadius: '95%', color: 'white' };
}else if (status === 'Invited') {
  return { backgroundColor: 'grey', borderRadius: '95%', color: 'white' };
}else if (status === 'Unverified') {
  return { backgroundColor: 'cornflowerblue', borderRadius: '95%', color: 'white' };
}else if (status === 'Pending') {
  return { backgroundColor: 'yellow', borderRadius: '95%', color: 'black' };
}
}
const sortTable = (n) => {
  // eslint-disable-next-line one-var
  
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById('data');
  console.log(table);
  switching = true;
  // Set the sorting direction to ascending:
  dir = 'asc';
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    console.log(table)
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName('TD')[n];
      y = rows[i + 1].getElementsByTagName('TD')[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir === 'asc') {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir === 'desc') {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == 'asc') {
        dir = 'desc';
        switching = true;
      }
    }
  }
}

  return (
    <div>
    <Navbar />
    <div class="databox">
        <div class="data">
           <div class ='content1'>Total Number of Users</div>
           <div class ='datainside'>
           <div class ='content2'>{tableData.length}</div>
            <div class='content2'style={{'color':'white'}}>blank</div>
            </div>
        </div>
        <div class="data">
        <div class ='content1'>Number of New Users This Month</div>
        <div class ='datainside'>
           <div class ='content2'>2</div>
           <div class='content2'>+50% compared to last month</div>
           </div>
        </div>
        <div class="data">
        <div class ='content1'>Number of Active Users This Month</div>
        <div class ='datainside'>
           <div class ='content2'>5</div>
           <div class='content2'>+20% compared to last month</div>
           </div>
        </div>
        <div class="data">
        <div class ='content1'>Average Session Duration</div>
        <div class ='datainside'>
           <div class ='content2'>1 hr and 30 min</div>
           <div class='content2' style={{color:'white'}}>+20% compared to last month</div>
           </div>
        </div>
    </div>
    <div class='dashboard'>
<div class='dashbar'>
    <div class='invite'>
  <button class='invitebutton'>
    Invite User
  </button>
    </div>
    <div class= 'searchbar'>
        <label class='search'>Search: </label>
    <input
    class="searchbox"
  type="text"
  placeholder="Search..."
  value={searchQuery}
  onChange={(event) => setSearchQuery(event.target.value)}
/>
<button class='searchby' onClick={handleSearchButtonClick}>
  Search By
</button>
{showSearchList && (
<div style={{display: 'flex', flexDirection:'column', justifyContent:'center', alignItems:'center', marginTop:'2%'}}><label htmlFor="mySelect"></label>
      <select id="mySelect" value={selectedOption} onChange={handleSelectChange}>
        <option value="">-- Select an option --</option>
        <option value="First Name">First Name</option>
        <option value="Last Name">Last Name</option>
        <option value="Email">Email</option>
        <option value="Organization">Organization</option>
        <option value="Status">Status</option>
      </select>
      <p>You selected: {selectedOption}</p>
    </div>)}
    </div>
    
</div>

    </div>
   <div class='datatable'> 
<table id='data'>
  <thead class='headers'>
    <tr >
        <th class="indheaders" value= '0' onClick={()=>sortTable(0)}>Id</th>
      <th class="indheaders" value="First Name" onClick={()=>sortTable(1)} >First Name</th>
      <th class="indheaders"onClick={()=>sortTable(2)} value="Last Name">Last Name</th>
      <th onClick={()=>sortTable(3)}class="indheaders">Email</th>
      <th onClick={()=>sortTable(4)} class="indheaders">Organization</th>
      <th onClick={()=>sortTable(5)} class="indheaders"># Submitted Observations</th>
      <th  onClick={()=>sortTable(6)} class="indheaders">Last Active</th>
      <th onClick={()=>sortTable(7)} class="indheaders">Created On</th>
      <th onClick={()=>sortTable(8)} class="indheaders">Status</th>
      <th onClick={()=>sortTable(9)} class="indheaders">User Role</th>
      <th class="indheaders">Edit</th>
      <th class="indheaders">Delete</th>
      <th class="indheaders">Ban</th>
    </tr>
  </thead>
  <tbody>
    {currentPageItems.map((item) => (
      <tr key={item.id}>
        <td class="tablecontent">{item.id}</td>
        <td  class="tablecontent">{item['First Name']}</td>
        <td  class="tablecontent">{item['Last Name']}</td>
        <td  class="tablecontent">{item.email}</td>
        <td class="tablecontent">{item.organization}</td>
        <td class="tablecontent">{item.numofobs}</td>
        <td class="tablecontent">{item.lastActive}</td>
        <td class="tablecontent">{item.createdOn}</td>
        <div class="verified">
        <td class="tablecontent2"style={getStatusColor(item.status)}>{item.status}</td></div>
        <td class="tablecontent">{item.userRole}</td>
        <td class="tablecontent"> <button class="edits"> <FaPencilAlt /></button> </td>
        <td class="tablecontent">
        <button class="edits" >
          <FaTrash />
        </button>
        </td>
        <td class="tablecontent">
        <button class="edits" >
          <FaBan />
        </button>
        </td>
      </tr>
    ))}
  </tbody>
</table>
</div>
<div class='pages'>
<ReactPaginate
  pageCount={pageCount}
  onPageChange={handlePageChange}
  containerClassName={'pagination'}
  activeClassName={'active'}
  previousLabel={<FontAwesomeIcon
    icon={faArrowLeft}
    className="arrow-left"
    style={{ cursor: 'pointer' }}
  />}
  nextLabel={<FontAwesomeIcon
    icon={faArrowRight}
    className="arrow-left"
    style={{ cursor: 'pointer' }}
  />}
/>
</div>
    </div>
  );
};
