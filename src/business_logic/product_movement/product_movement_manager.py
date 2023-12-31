from src.business_logic.report.report_manager import ReportManager
from src.models import  ProductMovement
from src import  db


class ProductMovementManager():
    def get_all_product_movement():
        return ProductMovement.query.all()
    
    def get_product_movement(id):
        movement = ProductMovement.query.get(id)
        return movement
             
    def add_edit_product_movement(request,movement):
        from_id = request.form['from']
        to_id = request.form['to']
        product_id = request.form['product']
        qty = request.form['qty']
        balance=ReportManager.get_product_balance()
        previous_movement = None
        for location, data in balance.items():
            for product in data['Products']:
                if product['Product ID'] == product_id and data['Location ID'] == from_id:
                    previous_movement = product
                    break
        if previous_movement is None:
            previous_movement = {'Qty': -10}
        if int(qty) > 0:
            if not movement:    
                if (from_id and to_id) or (from_id and not to_id):
                    if int(previous_movement['Qty']) >= int(qty):
                        new_product_movement = ProductMovement(
                            from_location_id=from_id,
                            to_location_id=to_id,
                            qty=qty,
                            product_id=product_id
                        )
                        db.session.add(new_product_movement)
                    else:
                        return False
                elif (to_id and not from_id):
                        new_product_movement = ProductMovement(
                            from_location_id=from_id,
                            to_location_id=to_id,
                            qty=qty,
                            product_id=product_id
                        )
                        db.session.add(new_product_movement)  
                else:
                    return False        
            else:
               if ((from_id and to_id) or (from_id and not to_id) or (to_id and not from_id)) : 
                    movement.from_location_id = from_id
                    movement.to_location_id = to_id
                    movement.product_id = product_id
                    movement.qty = qty 
               else: 
                   return False      
            try:
                db.session.commit()
                return True
            except Exception:
                db.session.rollback()
                return False             
        else:
            return False

    def delete_product_movement(id):
        movement = ProductMovement.query.filter_by(movement_id=id).first()
        try:
            db.session.delete(movement)
            db.session.commit()
            return True
        except Exception :
            db.session.rollback() 
            return False  
  
                    
    
