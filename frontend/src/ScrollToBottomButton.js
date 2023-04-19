

import React, { useState } from 'react';

function PdfViewerModal(props) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  function openModal() {
    setIsModalOpen(true);
    // eslint-disable-next-line no-console
    console.log('open')
    
  }

  function closeModal() {
    setIsModalOpen(false);
  }

  function scrollToBottom() {
    const iframe = document.getElementById('pdf-iframe');
    iframe.contentWindow.scrollTo(0, iframe.contentWindow.document.body.scrollHeight);
  }

  return (
    <>
      <button onClick={openModal}>Open PDF Viewer</button>
      {isModalOpen &&
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            <iframe id="pdf-iframe" src={props.pdfUrl} title='Privacy Policy'></iframe>
            <button onClick={scrollToBottom}>Scroll to bottom</button>
          </div>
        </div>
      }
    </>
  );
}

export default PdfViewerModal;