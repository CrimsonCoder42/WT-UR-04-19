/* eslint-disable no-console */
/* eslint-disable import/no-anonymous-default-export */
/* eslint-disable no-console */
/* eslint-disable no-useless-concat */
/* eslint-disable no-undef */
/* eslint-disable no-unused-vars, no-shadow */

import React, {useContext} from 'react';
import { Button } from 'antd';
import { ProfileContext } from '../../ProfilePage';
import  '../../styles/profile/profileStyles.css';


export default function WildTrackAccount() {
    const [profile] = useContext(ProfileContext);

    const deletes = () => {
        if (window.confirm('Are you sure you want to delete your profile?')) {
            console.log('Profile has been deleted');
            console.log(profile.id); // Log the ID of the user profile to be deleted
        } else {
            console.log('Your profile has not been deleted');
        }
    };

            return (
            <>

                    <div className='my-account-wrapper'

                    >

                        {/* Display user information */}

                            <h3 className={'profile-wt-title'}>My WildTrack Account</h3>


                        <span
                            // style={{
                            //     fontWeight: 'bold',
                            //     color: 'black',
                            //     fontSize: '10px',
                            // }}
                        >
            <i
                className='fa fa-user fa-5x icon'
                 // style={{ backgroundColor: 'white', color: '#348e47' }}
            ></i>
          </span>

                        <h4
                            // style={{
                            //     display: 'block',
                            //     margin: '50px auto',
                            //     width: '200px',
                            //     textAlign: 'center',
                            // }}
                        >
                            <b>Name: </b>
                            {`${profile?.first_name ?? ''} ${profile?.last_name ?? ''}`}
                        </h4>

                        <h4
                            // style={{
                            //     display: 'block',
                            //     margin: '50px auto',
                            //     width: '200px',
                            //     textAlign: 'center',
                            //     fontSize: '14px',
                            // }}
                        >
                            <b>Role: </b>
                            {profile?.position}
                        </h4>

                        <h4
                            // style={{
                            //     display: 'block',
                            //     margin: '50px auto',
                            //     width: '200px',
                            //     textAlign: 'center',
                            // }}
                        >
                            <b>Created: </b>
                            {profile?.created}
                        </h4>

                        <h4
                            // style={{
                            //     display: 'block',
                            //     margin: '50px auto',
                            //     width: '200px',
                            //     textAlign: 'center',
                            //     fontSize: '14px',
                            // }}
                        >
                            <b>Updated: </b>
                            {profile?.updated}
                        </h4>

                        <button
                            // style={{
                            //     backgroundColor: 'red',
                            //     color: 'white',
                            //     border: 'none',
                            //     paddingTop: '5px',
                            //     paddingBottom: '5px',
                            //     paddingRight: '15px',
                            //     paddingLeft: '15px',
                            // }}
                            type='button'
                            onClick={deletes}
                        >
                            Delete Account
                        </button>
                    </div>

            </>
                        );
}
