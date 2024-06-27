import React, { useState, useEffect, useCallback } from 'react';
import { Table, Select, message } from 'antd';
import { getUsers, updateUserRoles, getRoles } from '../../services/api';

const { Option } = Select;

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const response = await getUsers();
      setUsers(response.data);
    } catch (error) {
      message.error('Failed to fetch users');
    }
    setLoading(false);
  }, []);

  const fetchRoles = useCallback(async () => {
    try {
      const response = await getRoles();
      setRoles(response.data);
    } catch (error) {
      message.error('Failed to fetch roles');
    }
  }, []);

  useEffect(() => {
    fetchUsers();
    fetchRoles();
  }, [fetchUsers, fetchRoles]);

  const handleRoleChange = async (userId, newRoles) => {
    try {
      await updateUserRoles(userId, newRoles);
      message.success('User roles updated successfully');
      fetchUsers(); // Refresh the user list
    } catch (error) {
      message.error('Failed to update user roles');
    }
  };

  const columns = [
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Roles',
      dataIndex: 'roles',
      key: 'roles',
      render: (userRoles, record) => (
        <Select
          mode="multiple"
          style={{ width: '100%' }}
          placeholder="Select roles"
          value={userRoles.map(role => role.name)}
          onChange={(newRoles) => handleRoleChange(record.id, newRoles)}
        >
          {roles.map(role => (
            <Option key={role.id} value={role.name}>{role.name}</Option>
          ))}
        </Select>
      ),
    },
  ];

  return (
    <Table
      loading={loading}
      columns={columns}
      dataSource={users}
      rowKey="id"
    />
  );
}

export default UserManagement;