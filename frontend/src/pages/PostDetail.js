import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Spin, message } from 'antd';
import { getPostById } from '../services/api';

function PostDetail() {
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();

  const fetchPost = useCallback(async () => {
    try {
      setLoading(true);
      const response = await getPostById(id);
      setPost(response.data);
    } catch (error) {
      console.error('Failed to fetch post:', error);
      message.error('Failed to load post details');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchPost();
  }, [fetchPost]);

  if (loading) {
    return <Spin size="large" />;
  }

  return (
    <Card title={post?.title}>
      <p>{post?.content}</p>
    </Card>
  );
}

export default PostDetail;