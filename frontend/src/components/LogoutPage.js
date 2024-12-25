import { useAuth } from '../AuthContext'
import { useNavigate } from 'react-router-dom';

const LogoutPage = () => {
  const { clearTokens } = useAuth();
  const navigate = useNavigate();

  clearTokens();

  navigate('/login');
};

export default LogoutPage;
