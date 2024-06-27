import React from 'react';
import { Form, Input, Button, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const onFinish = async (values) => {
    try {
      await login(values);
      message.success('Login successful');
      navigate('/posts');
    } catch (error) {
      console.error('Login error:', error);
      if (error.response) {
        // 服务器响应了请求，但返回了错误状态码
        console.log('Error response:', error.response);
        message.error(`Login failed: ${error.response.data?.detail || 'Unknown error'}`);
      } else if (error.request) {
        // 请求已经发出，但没有收到响应
        console.log('Error request:', error.request);
        message.error('No response from server. Please try again later.');
      } else {
        // 发生了一些错误，阻止了请求的发送
        console.log('Error message:', error.message);
        message.error(`An error occurred: ${error.message}`);
      }
    }
  };

  return (
    <Form onFinish={onFinish}>
      <Form.Item name="username" rules={[{ required: true }]}>
        <Input placeholder="Username" />
      </Form.Item>
      <Form.Item name="password" rules={[{ required: true }]}>
        <Input.Password placeholder="Password" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">Login</Button>
      </Form.Item>
    </Form>
  );
}

export default LoginPage;