import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterBusiness: React.FC = () => {
  const navigate = useNavigate();

  // Redirect to the new create business page
  useEffect(() => {
    navigate('/create-business');
  }, [navigate]);

  return null;
};

export default RegisterBusiness;