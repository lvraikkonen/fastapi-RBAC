import React, { useState, useEffect, useCallback } from 'react';
import { Form, Input, Button, message, Spin, Descriptions } from 'antd';
import { getCurrentUser, updateCurrentUser } from '../services/api';

function Profile() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(true);
  const [userInfo, setUserInfo] = useState(null);
  const [editing, setEditing] = useState(false);

  const fetchUserProfile = useCallback(async () => {
    try {
      setLoading(true);
      const response = await getCurrentUser();
      setUserInfo(response.data);
      form.setFieldsValue(response.data);
    } catch (error) {
      message.error('Failed to fetch user profile');
      console.error('Fetch profile error:', error);
    } finally {
      setLoading(false);
    }
  }, [form]);

  useEffect(() => {
    fetchUserProfile();
  }, [fetchUserProfile]);

  const onFinish = async (values) => {
    try {
      await updateCurrentUser(values);
      message.success('Profile updated successfully');
      setEditing(false);
      fetchUserProfile(); // Refresh user info after update
    } catch (error) {
      message.error('Failed to update profile');
      console.error('Update profile error:', error);
    }
  };

  if (loading) {
    return <Spin size="large" />;
  }

  return (
    <div>
      {!editing ? (
        <>
          <Descriptions title="User Profile" bordered>
            <Descriptions.Item label="Username">{userInfo?.username}</Descriptions.Item>
            <Descriptions.Item label="Email">{userInfo?.email}</Descriptions.Item>
            <Descriptions.Item label="Full Name">{userInfo?.full_name}</Descriptions.Item>
            {/* Add more fields as needed */}
          </Descriptions>
          <Button type="primary" onClick={() => setEditing(true)} style={{ marginTop: 16 }}>
            Edit Profile
          </Button>
        </>
      ) : (
        <Form form={form} onFinish={onFinish} layout="vertical">
          <Form.Item
            name="username"
            label="Username"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input disabled />
          </Form.Item>
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: 'Please input your email!' },
              { type: 'email', message: 'Please enter a valid email!' }
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="full_name"
            label="Full Name"
            rules={[{ required: true, message: 'Please input your full name!' }]}
          >
            <Input />
          </Form.Item>
          {/* Add more form items as needed */}
          <Form.Item>
            <Button type="primary" htmlType="submit">
              Update Profile
            </Button>
            <Button onClick={() => setEditing(false)} style={{ marginLeft: 8 }}>
              Cancel
            </Button>
          </Form.Item>
        </Form>
      )}
    </div>
  );
}

export default Profile;