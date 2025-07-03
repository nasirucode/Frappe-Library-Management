# Copyright (c) 2025, Isyaku Murtala and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.password import update_password
import random
import string


class Librarian(Document):
    def validate(self):
        """Validate librarian data before saving"""
        self.validate_email()
    
    def before_insert(self):
        """Create or link user before inserting librarian record"""
        self.setup_user()
    
    def validate_email(self):
        """Validate that email is provided"""
        if not self.email:
            frappe.throw(_("Email is required for Librarian"))
    
    def setup_user(self):
        """Create new user or link existing user to librarian"""
        if not self.email:
            return
            
        existing_user = frappe.db.get_value("User", {"email": self.email}, "name")
        
        if existing_user:
            self.user = existing_user
            self.ensure_librarian_role(existing_user)
            frappe.msgprint(_("Linked to existing user: {0}").format(existing_user))
        else:
            self.user = self.create_new_user()
    
    def create_new_user(self):
        """Create a new user with librarian role and strong default password"""
        try:
            username = self.get_username()
            default_password = self.generate_strong_password()
            
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": self.email,
                "username": username,
                "first_name": self.first_name or self.get_fallback_first_name(),
                "last_name": self.last_name or "",
                "mobile_no": self.mobile,
                "gender": self.gender,
                "middle_name": self.middle_name or "",
                "send_welcome_email": 0,  # No email
                "enabled": 1,
                "roles": [{"role": "Librarian"}]
            })
            user_doc.insert(ignore_permissions=True)
            
            # Set the password after user creation
            update_password(user_doc.name, default_password)
            
            # Display credentials to admin
            self.show_login_credentials(username, default_password)
            
            return user_doc.name
            
        except Exception as e:
            frappe.throw(_("Failed to create user: {0}").format(str(e)))
    
    def generate_strong_password(self):
        """Generate a strong password that meets Frappe's requirements"""
        
        # Method 1: Pattern-based strong password
        first_name = (self.first_name or "User").title()
        
        # Create a strong password: FirstName + Special + Numbers + Lowercase
        # Example: John@2025lib
        password = f"{first_name}@{random.randint(1000, 9999)}lib"
        
        return password
        
        # Alternative Method 2: Completely random but memorable
        # adjectives = ['Quick', 'Smart', 'Bright', 'Swift', 'Clear', 'Sharp', 'Bold']
        # special_chars = ['@', '#', '$', '&']
        # adjective = random.choice(adjectives)
        # special = random.choice(special_chars)
        # number = random.randint(100, 999)
        # suffix = random.choice(['lib', 'book', 'read'])
        # return f"{adjective}{special}{number}{suffix}"
        
        # Alternative Method 3: Truly random strong password
        # length = 10
        # characters = string.ascii_letters + string.digits + "@#$&"
        # return ''.join(random.choice(characters) for _ in range(length))
    
    def show_login_credentials(self, username, password):
        """Display login credentials to admin"""
        frappe.msgprint(
            _("""
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #28a745;">
                <h4 style="color: #28a745; margin-top: 0;">✅ Librarian Account Created Successfully!</h4>
                
                <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <h5>🔑 Login Credentials:</h5>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; font-weight: bold; width: 30%;">Username:</td>
                            <td style="padding: 8px; background: #e9ecef; font-family: monospace; border-radius: 3px;"><strong>{0}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold;">Email:</td>
                            <td style="padding: 8px; background: #e9ecef; font-family: monospace; border-radius: 3px;"><strong>{1}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold;">Password:</td>
                            <td style="padding: 8px; background: #fff3cd; font-family: monospace; border-radius: 3px; color: #856404; font-size: 16px;"><strong>{2}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold;">Login URL:</td>
                            <td style="padding: 8px; background: #e9ecef; font-family: monospace; border-radius: 3px;"><a href="{3}" target="_blank">{3}</a></td>
                        </tr>
                    </table>
                </div>
                
                <div style="background: #fff3cd; padding: 10px; border-radius: 5px; border-left: 3px solid #ffc107; margin-top: 10px;">
                    <strong>⚠️ Important:</strong> Please share these credentials securely with the librarian and ask them to change the password after first login.
                </div>
            </div>
            """).format(username, self.email, password, frappe.utils.get_url(), (self.first_name or "User").title()),
            title=_("Librarian Login Credentials"),
            indicator="green"
        )
    
    def ensure_librarian_role(self, user_email):
        """Ensure existing user has librarian role"""
        if not frappe.db.exists("Has Role", {"parent": user_email, "role": "Librarian"}):
            user_doc = frappe.get_doc("User", user_email)
            user_doc.append("roles", {"role": "Librarian"})
            user_doc.save(ignore_permissions=True)
    
    def get_username(self):
        """Generate unique username from email"""
        base_username = self.email.split("@")[0]
        
        username = base_username
        counter = 1
        
        while frappe.db.exists("User", {"username": username}):
            username = f"{base_username}{counter}"
            counter += 1
            
        return username
    
    def get_fallback_first_name(self):
        """Get fallback first name from email if first_name is not provided"""
        return self.email.split("@")[0].title()
