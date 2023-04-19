import React, {useState} from 'react';
import privacy from './Privacy.pdf'

function PrivacyPolicyModal(props) {
  const [agreed, setAgreed] = useState(false);

  const handleAgree = () => {
    setAgreed(true);
    props.onAgree();
    
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>Privacy Policy</h2>
        <iframe src={privacy} width="100%" height="400px"></iframe>
        <div>
          <label>
            {agreed}
            <input type="checkbox" onChange={handleAgree} />
            I have read and agree to the Privacy Policy
          </label>
        </div>
      </div>
    </div>
  );
}

export default PrivacyPolicyModal;