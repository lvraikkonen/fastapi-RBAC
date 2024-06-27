import React from 'react';
import { Layout, Menu, Button } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Header, Content, Footer } = Layout;

function AppLayout({ children }) {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header>
        <div className="logo" />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="1"><Link to="/posts">Posts</Link></Menu.Item>
          {isAuthenticated && <Menu.Item key="2"><Link to="/profile">Profile</Link></Menu.Item>}
          {isAdmin && <Menu.Item key="3"><Link to="/admin">Admin</Link></Menu.Item>}
        </Menu>
        {isAuthenticated ? (
          <Button onClick={handleLogout} style={{ float: 'right', marginTop: '15px' }}>
            Logout ({user.username})
          </Button>
        ) : (
          <Button onClick={() => navigate('/login')} style={{ float: 'right', marginTop: '15px' }}>
            Login
          </Button>
        )}
      </Header>
      <Content style={{ padding: '0 50px', marginTop: 64 }}>
        <div className="site-layout-content" style={{ background: '#fff', padding: 24, minHeight: 380 }}>
          {children}
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>RBAC Frontend ©2024 Created by Your Name</Footer>
    </Layout>
  );
}

export default AppLayout;