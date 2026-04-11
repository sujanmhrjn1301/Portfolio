import React from 'react';

const modalStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100vw',
  height: '100vh',
  background: 'rgba(0,0,0,0.7)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 9999,
};

const boxStyle = {
  background: '#18181b',
  color: '#fff',
  padding: '2rem 2.5rem',
  borderRadius: '1rem',
  boxShadow: '0 4px 32px rgba(0,0,0,0.25)',
  textAlign: 'center',
  minWidth: '260px',
};

export default function BackendWaitModal() {
  return (
    <div style={modalStyle}>
      <div style={boxStyle}>
        <h2 style={{marginBottom: '1rem'}}>Please wait for a while before chatting</h2>
        <div style={{fontSize: '1.1rem', color: '#a3a3a3'}}>Connecting to backend server...</div>
      </div>
    </div>
  );
}
