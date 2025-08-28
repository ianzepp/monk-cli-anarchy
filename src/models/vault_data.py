"""
VAULT-TEC ENTERPRISE SUITE™
Mock Data Generator for Development/Demo Mode

"Realistic vault operations data... simulated for your convenience."
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any


class VaultDataGenerator:
    """Generates realistic mock data for vault operations"""
    
    VAULT_PERSONNEL = [
        "LONE_WANDERER", "THREE_DOG", "SARAH_LYONS", "ELDER_LYONS", 
        "KNIGHT_CAPTAIN", "PALADIN_CROSS", "FAWKES", "CHARON",
        "DOGMEAT", "BUTCH_DELORIA", "AMATA", "JAMES_FATHER",
        "MR_BURKE", "LUCAS_SIMMS", "NOVA", "GRETA"
    ]
    
    VAULT_SECTIONS = [
        "OVERSEER", "SECURITY", "MEDICAL", "ENGINEERING", 
        "MAINTENANCE", "RESEARCH", "COMMUNICATIONS", "HYDROPONICS",
        "ARCHIVES", "RECREATION", "QUARTERS", "STORAGE"
    ]
    
    SCHEMA_NAMES = [
        "personnel_records", "security_clearance", "inventory_management",
        "medical_records", "facility_maintenance", "research_data",
        "communication_logs", "supply_requisitions", "incident_reports",
        "vault_operations", "environmental_data", "power_systems"
    ]
    
    ACTIVITY_TYPES = {
        "PERSONNEL": ["CREATE", "UPDATE", "DELETE", "TRANSFER"],
        "SECURITY": ["UPDATE", "VERIFY", "RESTRICT", "GRANT"],
        "INVENTORY": ["CREATE", "UPDATE", "DELETE", "AUDIT"],
        "SCHEMA": ["DEPLOY", "UPDATE", "VALIDATE", "ROLLBACK"],
        "OBSERVER": ["INFO", "WARNING", "ERROR", "RECOVERY"],
        "SYSTEM": ["BACKUP", "MAINTENANCE", "UPGRADE", "MONITOR"]
    }

    def __init__(self):
        self.start_time = datetime.now() - timedelta(hours=8)
        self.activity_counter = 0

    def generate_system_status(self) -> Dict[str, str]:
        """Generate mock system status"""
        statuses = ["ok", "warning", "error"]
        weights = [0.8, 0.15, 0.05]  # 80% ok, 15% warning, 5% error
        
        return {
            "database": random.choices(statuses, weights=weights)[0],
            "api": random.choices(statuses, weights=[0.9, 0.08, 0.02])[0],
            "observers": random.choices(statuses, weights=[0.85, 0.12, 0.03])[0],
            "security": random.choices(statuses, weights=[0.95, 0.04, 0.01])[0]
        }

    def generate_population_stats(self) -> Dict[str, Any]:
        """Generate mock population statistics"""
        total = random.randint(2800, 3200)
        offline = random.randint(10, 50)
        active = total - offline
        
        return {
            "total": total,
            "active": active, 
            "offline": offline,
            "last_update": datetime.now().strftime("%H:%M:%S")
        }

    def generate_alerts(self) -> List[Dict[str, Any]]:
        """Generate mock alert data"""
        alerts = []
        
        # Schema warnings
        if random.random() < 0.3:
            alerts.append({
                "type": "schema",
                "level": "warning",
                "message": "Schema validation performance degraded",
                "timestamp": datetime.now().isoformat()
            })
        
        # Critical alerts (rare)
        if random.random() < 0.05:
            alerts.append({
                "type": "system",
                "level": "critical",
                "message": "Database connection pool exhausted",
                "timestamp": datetime.now().isoformat()
            })
            
        # Informational alerts
        if random.random() < 0.4:
            alerts.append({
                "type": "observer",
                "level": "info", 
                "message": "Observer pipeline processing normally",
                "timestamp": datetime.now().isoformat()
            })
            
        return alerts

    def generate_recent_activity(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate mock recent activity entries"""
        activities = []
        
        for i in range(count):
            module = random.choice(list(self.ACTIVITY_TYPES.keys()))
            action = random.choice(self.ACTIVITY_TYPES[module])
            
            # Generate timestamp (recent activities)
            timestamp = self.start_time + timedelta(
                minutes=random.randint(0, 480),  # Last 8 hours
                seconds=random.randint(0, 59)
            )
            
            # Generate description based on module/action
            description = self._generate_activity_description(module, action)
            
            activities.append({
                "timestamp": timestamp.strftime("%H:%M:%S"),
                "module": module,
                "action": action,
                "description": description,
                "user": "root"  # For now, always root in overseer mode
            })
            
        # Sort by timestamp (most recent first)
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities

    def _generate_activity_description(self, module: str, action: str) -> str:
        """Generate realistic activity descriptions"""
        if module == "PERSONNEL":
            if action == "CREATE":
                resident = random.choice(self.VAULT_PERSONNEL)
                return f"New resident: {resident}"
            elif action == "UPDATE":
                return "Security clearance modified"
            elif action == "DELETE":
                return "Resident record archived"
            else:
                section = random.choice(self.VAULT_SECTIONS)
                return f"Transfer to {section} section"
                
        elif module == "SECURITY":
            if action == "UPDATE":
                return "Access level modified"
            elif action == "VERIFY":
                return "Biometric scan completed"
            else:
                return f"Clearance {action.lower()}ed"
                
        elif module == "INVENTORY":
            items = ["STIMPAK", "RAD-AWAY", "PLASMA_RIFLE", "POWER_ARMOR", "NUKA_COLA"]
            item = random.choice(items)
            if action == "CREATE":
                return f"Equipment added: {item}"
            elif action == "DELETE":
                return f"Equipment decommissioned: {item}"
            else:
                return f"Inventory {action.lower()}: {item}"
                
        elif module == "SCHEMA":
            schema = random.choice(self.SCHEMA_NAMES)
            version = f"v{random.randint(1,3)}.{random.randint(0,5)}.{random.randint(0,10)}"
            return f"{schema} {version}"
            
        elif module == "OBSERVER":
            if action == "INFO":
                return "All security rings active"
            elif action == "WARNING":
                return "Performance threshold exceeded"
            else:
                return f"Observer ring {action.lower()}"
                
        else:  # SYSTEM
            operations = {
                "BACKUP": "System backup completed",
                "MAINTENANCE": "Scheduled maintenance performed", 
                "UPGRADE": "Component upgrade installed",
                "MONITOR": "Health check completed"
            }
            return operations.get(action, f"System {action.lower()}")

    def generate_schema_registry_data(self) -> List[Dict[str, Any]]:
        """Generate mock schema registry data"""
        schemas = []
        
        for i, name in enumerate(self.SCHEMA_NAMES):
            status_options = ["●DEPLOYED", "⚠TESTING", "○DRAFT"]
            status_weights = [0.6, 0.25, 0.15]
            status = random.choices(status_options, weights=status_weights)[0]
            
            # Generate realistic version numbers
            major = random.randint(1, 3)
            minor = random.randint(0, 5)  
            patch = random.randint(0, 15)
            version = f"v{major}.{minor}.{patch}"
            
            # Generate record counts based on status
            if status == "●DEPLOYED":
                records = random.randint(100, 50000)
            elif status == "⚠TESTING":
                records = random.randint(10, 5000)
            else:  # DRAFT
                records = 0
                
            # Actions based on status
            if status == "●DEPLOYED":
                actions = "[E][D]"  # Edit, Deploy
            elif status == "⚠TESTING":
                actions = "[E][T]"  # Edit, Test
            else:  # DRAFT
                actions = "[E][X]"  # Edit, Delete
            
            schemas.append({
                "name": name,
                "version": version,
                "records": f"{records:,}" if records > 0 else "0",
                "status": status,
                "actions": actions,
                "record_count": records,
                "last_modified": self.start_time + timedelta(days=random.randint(0, 30))
            })
            
        # Sort by record count (most used first)
        schemas.sort(key=lambda x: x["record_count"], reverse=True)
        return schemas

    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate complete dashboard data set"""
        return {
            "system_status": self.generate_system_status(),
            "population_stats": self.generate_population_stats(),
            "alerts": self.generate_alerts(),
            "recent_activity": self.generate_recent_activity()
        }


# Global data generator instance
vault_data = VaultDataGenerator()