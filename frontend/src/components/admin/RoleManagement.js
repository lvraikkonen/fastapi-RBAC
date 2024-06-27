import React, { useState, useEffect, useCallback } from 'react';
import { Table, Button, Modal, Form, Input, message } from 'antd';
import { getRoles, createRole, updateRole, deleteRole } from '../../services/api';

function RoleManagement() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingRole, setEditingRole] = useState(null);

  const fetchRoles = useCallback(async () => {
    setLoading(true);
    try {
      const response = await getRoles();
      setRoles(response.data);
    } catch (error) {
      message.error('Failed to fetch roles');
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchRoles();
  }, [fetchRoles]);

  const handleCreateOrUpdate = async (values) => {
    try {
      if (editingRole) {
        await updateRole(editingRole.id, values);
        message.success('Role updated successfully');
      } else {
        await createRole(values);
        message.success('Role created successfully');
      }
      setModalVisible(false);
      fetchRoles();
    } catch (error) {
      message.error('Failed to save role');
    }
  };

  const handleDelete = async (roleId) => {
    try {
      await deleteRole(roleId);
      message.success('Role deleted successfully');
      fetchRoles();
    } catch (error) {
      message.error('Failed to delete role');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button onClick={() => {
            setEditingRole(record);
            form.setFieldsValue(record);
            setModalVisible(true);
          }}>Edit</Button>
          <Button onClick={() => handleDelete(record.id)} danger>Delete</Button>
        </>
      ),
    },
  ];

  return (
    <>
      <Button onClick={() => {
        setEditingRole(null);
        form.resetFields();
        setModalVisible(true);
      }} type="primary" style={{ marginBottom: 16 }}>
        Create New Role
      </Button>
      <Table
        loading={loading}
        columns={columns}
        dataSource={roles}
        rowKey="id"
      />
      <Modal
        title={editingRole ? "Edit Role" : "Create New Role"}
        visible={modalVisible}
        onOk={form.submit}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} onFinish={handleCreateOrUpdate}>
          <Form.Item name="name" rules={[{ required: true }]}>
            <Input placeholder="Role Name" />
          </Form.Item>
          <Form.Item name="description">
            <Input.TextArea placeholder="Description" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}

export default RoleManagement;