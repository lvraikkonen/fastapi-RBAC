import React from 'react';
import { Tabs } from 'antd';
import UserManagement from '../components/admin/UserManagement';
import RoleManagement from '../components/admin/RoleManagement';
import PermissionManagement from '../components/admin/PermissionManagement';

const { TabPane } = Tabs;

function AdminDashboard() {
  return (
    <Tabs defaultActiveKey="1">
      <TabPane tab="User Management" key="1">
        <UserManagement />
      </TabPane>
      <TabPane tab="Role Management" key="2">
        <RoleManagement />
      </TabPane>
      <TabPane tab="Permission Management" key="3">
        <PermissionManagement />
      </TabPane>
    </Tabs>
  );
}

export default AdminDashboard;