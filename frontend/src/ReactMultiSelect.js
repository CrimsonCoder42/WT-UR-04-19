import React, { useState} from 'react'
import { MultiSelect } from 'react-multi-select-component';
import countries from './multiselect.json'

const dictionary = countries.countries

const DisabledPage = () => {
    const [selected, setSelected] = useState([]);
  
    return (
      <div>
 
        <MultiSelect 
        
          options={dictionary}
          value={selected}
          onChange={setSelected}
          labelledBy="Select"
          disabled
        />
      </div>
    );
  };
  
  export default DisabledPage;