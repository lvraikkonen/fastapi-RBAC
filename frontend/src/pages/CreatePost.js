// src/pages/CreatePost.js
import React from 'react';
import { Form, Input, Button, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { createPost } from '../services/api';

const { TextArea } = Input;

function CreatePost() {
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      await createPost(values);
      message.success('Post created successfully');
      navigate('/posts');
    } catch (error) {
      message.error('Failed to create post');
      console.error('Create post error:', error);
    }
  };

  return (
    <Form onFinish={onFinish} layout="vertical">
      <Form.Item
        name="title"
        label="Title"
        rules={[{ required: true, message: 'Please input the title!' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        name="content"
        label="Content"
        rules={[{ required: true, message: 'Please input the content!' }]}
      >
        <TextArea rows={4} />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Create Post
        </Button>
      </Form.Item>
    </Form>
  );
}

export default CreatePost;