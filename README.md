# fastapi-RBAC

以下是按功能区域划分的API概览：

## 认证和用户管理

```
POST /api/v1/token：用户登录，获取访问令牌
POST /api/v1/register/：注册新用户
GET /api/v1/users/me：获取当前登录用户信息
PUT /api/v1/users/me：更新当前登录用户信息
```


## 帖子管理

```
POST /api/v1/posts/：创建新帖子
GET /api/v1/posts/：获取帖子列表
GET /api/v1/posts/{post_id}：获取特定帖子详情
```

## 角色和权限查看（需要相应权限）

```
GET /api/v1/roles：获取所有角色列表
GET /api/v1/permissions：获取所有权限列表
```

## 管理功能（仅限管理员访问）

### 用户管理：

```
GET /api/v1/admin/users：获取所有用户列表
PUT /api/v1/admin/users/{user_id}/roles：更新指定用户的角色
```

### 角色管理：

```
POST /api/v1/admin/roles：创建新角色
GET /api/v1/admin/roles：获取所有角色
PUT /api/v1/admin/roles/{role_id}：更新指定角色
DELETE /api/v1/admin/roles/{role_id}：删除指定角色
```

### 权限管理：

```
POST /api/v1/admin/permissions：创建新权限
GET /api/v1/admin/permissions：获取所有权限
PUT /api/v1/admin/permissions/{permission_id}：更新指定权限
DELETE /api/v1/admin/permissions/{permission_id}：删除指定权限
```


## 前端程序结构：

- 用户认证和授权模块
- 管理员管理界面
- 普通用户界面
- 公共组件
