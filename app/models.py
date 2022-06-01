from . import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30))
    permissions = db.Column(db.Integer)
    default_role = db.Column(db.Boolean, default=False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def has_permission(self, perm):
        return (self.permissions & perm)  == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm 

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm 
    
    def reset_permission(self):
        self.permissions = 0

    def insert_role():
        roles = {
            'User' : [Permission.FOLLOW, Permission.WRITE, Permission.COMMENT],
            'Admin' :  [Permission.FOLLOW, Permission.WRITE, Permission.COMMENT , Permission.ADMIN]
        }

        for ro in roles:
            role = Role.query.filter_by(role_name = ro).first()
            if role is None:
                role = Role(role_name = ro)

            default_role = 'User'
            role.reset_permission()
            for perm in roles[ro]:
                role.add_permission(perm)
            role.default_role = (role.role_name == default_role)
            db.session.add(role)

        db.session.commit()
            


    def __repr__(self):
        return f'<{self.__class__.__name__} {self.role_name}>'


class Permission:
    FOLLOW = 1 
    WRITE = 2
    COMMENT = 4 
    ADMIN = 8