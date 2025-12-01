import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterBusiness: React.FC = () => {
  const navigate = useNavigate();
  
  // Redirect to register page since business registration is now part of the multi-step form
  useEffect(() => {
    navigate('/register');
  }, [navigate]);

  return null;
};

export default RegisterBusiness;