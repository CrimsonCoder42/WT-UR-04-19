/* eslint-disable no-console */
/* eslint-disable import/no-anonymous-default-export */
/* eslint-disable no-console */
/* eslint-disable no-useless-concat */
/* eslint-disable no-undef */
/* eslint-disable no-unused-vars, no-shadow */
import { Form, Input, Button } from 'antd';
import React, { createContext, useState, useEffect } from 'react';
import Navbar from './Navbarloggedin';
import countries from './countries.json';
import DisabledPage from './ReactMultiSelect';
import useFetch from './hooks/useFetch';
import WildTrackAccount from './components/profile/wildTrackAccount.js';
import WildTrackEditAccount from './components/profile/wildTrackEditAccount.js';
import './styles/profile/profileStyles.css';

export const ProfileContext = createContext();

// don't put jsx inside of a state
export default function () {
    const ACCESS_TOKEN =
        sessionStorage.getItem('token')

// Define state variables for the editing mode and the user profile
    const [isEditingMode, setIsEditingMode] = useState(false);
    const [profile, setProfile] = useState({});

// Fetch the user profile data using the useFetch hook
    const { data, loading, error } = useFetch(
        'https://rtvb5hreoe.execute-api.us-east-1.amazonaws.com/dev/_api/v1/get_user'
    );

// Update the profile state variable when the data changes
    useEffect(() => {
        if (data) {
            const fetchedProfile = {
                first_name: data.first_name,
                last_name: data.last_name,
                organization: data.organization,
                position: data.position,
                role: data.role,
                interests: data.interests,
                country: data.country_of_residence,
                fieldwork_locations: data.fieldwork_locations,
                linkedin: data.linkedin,
                facebook: data.facebook,
                twitter: data.twitter,
                created: data.created,
                updated: data.updated
            };
            setProfile(fetchedProfile);
        }
    }, [data]);

// Define state variables for the submit loading status and any submit errors
    const [submitLoading, setSubmitLoading] = useState(false);
    const [submitError, setSubmitError] = useState(null);

// Define a function to set the editing mode to false
    const undo = function () {
        setIsEditingMode(false);
    };



// If the data is loading, display a loading message
    if (loading) {
        return <div>Loading...</div>;
    }

// If there is an error, display an error message
    if (error) {
        return <div>Error: {error}</div>;
    }

// Define a function to render the list of countries as <option> elements
    const renderCountries = () =>
        countries.countries.map((country) => {
            return <option value={country.name}>{country.name}</option>;
        });


    // Render profile page content
    return (
        <>

        <Navbar />
        <div class='wrapper'>

            <div
                 className='container'
            >
                <ProfileContext.Provider value={[profile, setProfile]}>
                  <div className={'wildTrackAccount'}><WildTrackAccount /></div>
                    <div className={'wildTrackEditAccount'}><WildTrackEditAccount /></div>
                </ProfileContext.Provider>
            </div>
        </div>
        </>
);
}