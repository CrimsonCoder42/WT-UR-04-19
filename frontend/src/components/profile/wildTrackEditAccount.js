/* eslint-disable no-console */
/* eslint-disable import/no-anonymous-default-export */
/* eslint-disable no-console */
/* eslint-disable no-useless-concat */
/* eslint-disable no-undef */
/* eslint-disable no-unused-vars, no-shadow */

import React, { useContext, useState } from 'react';
import { Form, Input, Button } from 'antd';
import { ProfileContext } from '../../ProfilePage';
import DisabledPage from '../../ReactMultiSelect'

export default function WildTrackEditAccount() {
    const [isEditingMode, setIsEditingMode] = useState(false);
    const [submitLoading, setSubmitLoading] = useState(false);
    const [submitError, setSubmitError] = useState(null);
    const [profile, setProfile] = useContext(ProfileContext);
    const [dropdown, setdropdown] = useState(<DisabledPage/>)

    const undo = () => {
        setIsEditingMode(false);
    };

    const renderCountries = () => {
        // Code to render the country options
    };

    // Define a function to handle the form submission
    const handleSubmit = async (values) => {
        setSubmitLoading(true); // Set the submit loading status to true
        setSubmitError(null); // Reset any previous submit errors
        console.log(values);

        try {
            const ACCESS_TOKEN =
                sessionStorage.getItem('token')

            // Send a POST request to update the user profile with the new values
            const response = await fetch(
                'https://rtvb5hreoe.execute-api.us-east-1.amazonaws.com/dev/_api/v1/update_user',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${ACCESS_TOKEN}`,
                    },
                    body: JSON.stringify(values), // Send the form values as a JSON string in the request body
                }
            );

            if (!response.ok) {
                // If the response is not OK, throw an error
                throw new Error('Error updating profile');
            }

            const data = await response.json(); // Parse the response JSON data

            const userProfile = data.length && data[0] ? data[0] : {};

            // Update the profile state with the new values entered in the form
            setProfile({ ...profile, ...userProfile });
        } catch (error) {
            setSubmitError(error.message); // Set the submit error state variable to the error message
        } finally {
            setSubmitLoading(false); // Set the submit loading status to false
            setIsEditingMode(false); // Set the editing mode to false
        }
    };

    return (
        <>
        <Form onFinish={handleSubmit}>
        <div>
            <h3 className={'profile-wt-title'}>Edit WildTrack Profile</h3>
            <div

            ></div>
            <br />

            <Form.Item
                colon={false}
                className='Form-label'
                name='first_name'
                id='first_name'
                initialValue={profile?.first_name}
                label={
                    <h4>
                        <b>First Name</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    type="text"
                    placeholder={profile?.first_name ? profile.first_name : 'First Name'}
                />
            </Form.Item>
            <Form.Item
                colon={false}
                className='Form-label'
                name='last_name'
                id='last_name'
                initialValue={profile?.last_name}
                label={
                    <h4>
                        <b>Last Name</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    placeholder={profile?.last_name ? profile.last_name : 'Last Name'}
                />
            </Form.Item>

            <Form.Item
                colon={false}
                className='Form-label'
                name='organization'
                id='organization'
                initialValue={profile?.organization}
                label={
                    <h4>
                        <b>Organization</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    placeholder={profile?.organization ? profile.organization : 'Last Name'}
                />
            </Form.Item>
            <Form.Item
                colon={false}
                className='Form-label'
                name='position'
                id='position'
                initialValue={profile?.position}
                label={
                    <h4>
                        <b>Position</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    placeholder={profile?.position ? profile.position : 'Position'}
                />
            </Form.Item>
            <Form.Item
                colon={false}
                className='Form-label'
                name='interests'
                id='interests'
                initialValue={profile?.interests}
                label={
                    <h4>
                        <b>Interests</b>
                    </h4>
                }
            >
          <textarea
              disabled={!isEditingMode}
              class='ant-input css-dev-only-do-not-override-1km3mtt'
              maxLength={10}
              placeholder={profile?.interests ? profile.interests : 'Position'}
              type='textarea'
          />
            </Form.Item>

            <Form.Item
                colon={false}
                className='Form-label'
                name='country'
                id='country'
                initialValue={profile?.country}
                label={
                    <h4>
                        <b>
                            Country Of Primary
                            <br /> Residence
                        </b>
                    </h4>
                }
            >
                <div class='ant-form-item-control-input-content'>
                    <select
                        disabled={!isEditingMode}
                        class='ant-input css-dev-only-do-not-override-1km3mtt'
                        name='countrieselect'
                        id='countryselect'
                        placeholder={profile?.country ? profile.country : 'Country'}

                    >
                        {renderCountries()}
                    </select>
                </div>
            </Form.Item>

            <Form.Item
                colon={false}
                className='Form-label'
                name='fieldwork_locations'
                id='fieldwork_locations'
                initialValue={profile?.fieldwork_locations}
                label={
                    <h4>
                        <b>Fieldwork Locations</b>
                    </h4>
                }
            >
                {dropdown}
            </Form.Item>

            <Form.Item
                colon={false}
                className='Form-label'
                name='linkedin'
                id='linkedin'
                initialValue={profile?.linkedin}
                label={
                    <h4>
                        <b>LinkedIn</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    placeholder={profile?.linkedin ? profile.linkedin : 'LinkedIn'}
                />
            </Form.Item>

            <Form.Item
                colon={false}
                className='Form-label'
                name='facebook'
                id='facebook'
                initialValue={profile?.facebook}
                label={
                    <h4>
                        <b>Facebook</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    placeholder={profile?.facebook ? profile.facebook : 'Facebook'}
                />
            </Form.Item>

            <Form.Item
                colon={false}
                className='Form-label'
                name='twitter'
                id='twitter'
                initialValue={profile?.twitter}
                label={
                    <h4>
                        <b>Twitter</b>
                    </h4>
                }
            >
                <Input
                    readOnly={!isEditingMode}
                    maxLength={10}
                    placeholder={profile?.twitter ? profile.twitter : 'Twitter'}
                />
            </Form.Item>

            <br />

            <div className='containing'

            >
                <div
                >
                    {!isEditingMode && (
                        <Button
                            type='primary'
                            htmlType='button'
                            onClick={() => setIsEditingMode(true)}
                            style={{marginRight: '20px'}}
                        >
                            Edit Profile
                        </Button>
                    )}

                    {isEditingMode && (
                        <Button
                            type='primary'
                            htmlType='button'
                            onClick={undo}
                            loading={submitLoading}
                        >
                            Undo
                        </Button>
                    )}

                    {isEditingMode && (
                        <Button type='primary' htmlType='submit' loading={submitLoading}>
                            {submitLoading ? 'Updating...' : 'Update Profile'}
                        </Button>
                    )}

                    {!!submitError && <p>{submitError}</p>}
                </div>
            </div>
        </div>

</Form>
        </>
)
}