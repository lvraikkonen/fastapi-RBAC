import React, { useState, useEffect, useCallback } from 'react';
import { Table, Button, Modal, Form, Input, message } from 'antd';
import { getPermissions, createPermission, updatePermission, deletePermission } from '../../services/api';

function PermissionManagement() {
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingPermission, setEditingPermission] = useState(null);

  const fetchPermissions = useCallback(async () => {
    setLoading(true);
    try {
      const response = await getPermissions();
      setPermissions(response.data);
    } catch (error) {
      message.error('Failed to fetch permissions');
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchPermissions();
  }, [fetchPermissions]);

  const handleCreateOrUpdate = async (values) => {
    try {
      if (editingPermission) {
        await updatePermission(editingPermission.id, values);
        message.success('Permission updated successfully');
      } else {
        await createPermission(values);
        message.success('Permission created successfully');
      }
      setModalVisible(false);
      fetchPermissions();
    } catch (error) {
      message.error('Failed to save permission');
    }
  };

  const handleDelete = async (permissionId) => {
    try {
      await deletePermission(permissionId);
      message.success('Permission deleted successfully');
      fetchPermissions();
    } catch (error) {
      message.error('Failed to delete permission');
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
            setEditingPermission(record);
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
        setEditingPermission(null);
        form.resetFields();
        setModalVisible(true);
      }} type="primary" style={{ marginBottom: 16 }}>
        Create New Permission
      </Button>
      <Table
        loading={loading}
        columns={columns}
        dataSource={permissions}
        rowKey="id"
      />
      <Modal
        title={editingPermission ? "Edit Permission" : "Create New Permission"}
        visible={modalVisible}
        onOk={form.submit}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} onFinish={handleCreateOrUpdate}>
          <Form.Item name="name" rules={[{ required: true }]}>
            <Input placeholder="Permission Name" />
          </Form.Item>
          <Form.Item name="description">
            <Input.TextArea placeholder="Description" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}

export default PermissionManagement;