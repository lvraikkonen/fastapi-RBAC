// src/pages/PostList.js
import React, { useState, useEffect } from 'react';
import { List, Button } from 'antd';
import { Link } from 'react-router-dom';
import { getPosts } from '../services/api';

function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await getPosts();
      setPosts(response.data);
    } catch (error) {
      console.error('Failed to fetch posts:', error);
    }
  };

  return (
    <div>
      <Button type="primary" style={{ marginBottom: 16 }}>
        <Link to="/posts/new">Create New Post</Link>
      </Button>
      <List
        itemLayout="horizontal"
        dataSource={posts}
        renderItem={(post) => (
          <List.Item
            actions={[<Link to={`/posts/${post.id}`}>View</Link>]}
          >
            <List.Item.Meta
              title={post.title}
              description={post.content.substring(0, 100) + '...'}
            />
          </List.Item>
        )}
      />
    </div>
  );
}

export default PostList;