# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import base64
import io
import csv
import json
import logging

_logger = logging.getLogger(__name__)


class PackingListImportWizard(models.TransientModel):
    _name = 'packing.list.import.wizard'
    _description = 'Wizard para Importar Packing List'
    
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de Compra',
        required=True,
        readonly=True
    )
    
    container_number = fields.Char(
        string='Número de Contenedor',
        required=True
    )
    
    commercial_invoice = fields.Char(
        string='Factura Comercial',
        required=True
    )
    
    packing_list_name = fields.Char(
        string='Nombre del Packing List',
        help='Nombre descriptivo para identificar este packing list'
    )
    
    import_method = fields.Selection([
        ('csv', 'Archivo CSV'),
        ('manual', 'Entrada Manual'),
        ('excel', 'Archivo Excel')
    ], string='Método de Importación', default='csv', required=True)
    
    # Campos para archivo
    import_file = fields.Binary(
        string='Archivo de Importación',
        help='Archivo CSV o Excel con los datos del packing list'
    )
    
    filename = fields.Char(
        string='Nombre del Archivo'
    )
    
    # Campos para entrada manual
    manual_data = fields.Text(
        string='Datos en JSON',
        help='Datos en formato JSON para entrada manual'
    )
    
    # Configuración de importación
    has_header = fields.Boolean(
        string='Archivo tiene encabezados',
        default=True,
        help='Marcar si la primera fila contiene encabezados'
    )
    
    delimiter = fields.Selection([
        (',', 'Coma (,)'),
        (';', 'Punto y coma (;)'),
        ('\t', 'Tabulador'),
        ('|', 'Pipe (|)')
    ], string='Delimitador', default=',')
    
    # Preview de datos
    preview_data = fields.Text(
        string='Vista Previa',
        readonly=True
    )
    
    # Estado del wizard
    step = fields.Selection([
        ('upload', 'Cargar Archivo'),
        ('preview', 'Vista Previa'),
        ('import', 'Importar')
    ], string='Paso', default='upload')
    
    # Mapeo de columnas
    column_mapping = fields.Text(
        string='Mapeo de Columnas',
        help='Mapeo de columnas en formato JSON'
    )
    
    @api.onchange('import_file', 'filename')
    def _onchange_import_file(self):
        """Generar vista previa cuando se carga un archivo"""
        if self.import_file and self.import_method in ['csv', 'excel']:
            try:
                preview = self._generate_preview()
                self.preview_data = preview
                if preview:
                    self.step = 'preview'
            except Exception as e:
                self.preview_data = f"Error al procesar archivo: {str(e)}"
    
    def _generate_preview(self):
        """Generar vista previa del archivo"""
        if not self.import_file:
            return ""
        
        try:
            file_content = base64.b64decode(self.import_file)
            
            if self.import_method == 'csv':
                return self._preview_csv(file_content)
            elif self.import_method == 'excel':
                return self._preview_excel(file_content)
                
        except Exception as e:
            return f"Error: {str(e)}"
        
        return ""
    
    def _preview_csv(self, file_content):
        """Vista previa de archivo CSV"""
        try:
            file_text = file_content.decode('utf-8')
            lines = file_text.split('\n')[:10]  # Primeras 10 líneas
            
            preview = "Vista previa (primeras 10 líneas):\n\n"
            for i, line in enumerate(lines, 1):
                if line.strip():
                    preview += f"{i:2d}: {line[:100]}...\n" if len(line) > 100 else f"{i:2d}: {line}\n"
            
            return preview
            
        except UnicodeDecodeError:
            try:
                file_text = file_content.decode('latin-1')
                lines = file_text.split('\n')[:5]
                preview = "Vista previa (encoding latin-1):\n\n"
                for i, line in enumerate(lines, 1):
                    if line.strip():
                        preview += f"{i}: {line[:100]}...\n" if len(line) > 100 else f"{i}: {line}\n"
                return preview
            except:
                return "Error: No se pudo decodificar el archivo. Verifique el encoding."
    
    def _preview_excel(self, file_content):
        """Vista previa de archivo Excel"""
        try:
            # Aquí se implementaría la lectura de Excel con openpyxl o xlrd
            return "Vista previa de Excel no implementada aún. Use CSV por favor."
        except Exception as e:
            return f"Error leyendo Excel: {str(e)}"
    
    def action_import_packing_list(self):
        """Procesar la importación del packing list"""
        self.ensure_one()
        
        if self.import_method == 'csv':
            return self._import_from_csv()
        elif self.import_method == 'manual':
            return self._import_from_manual()
        elif self.import_method == 'excel':
            return self._import_from_excel()
        else:
            raise UserError("Método de importación no soportado.")
    
    def _import_from_csv(self):
        """Importar desde archivo CSV"""
        if not self.import_file:
            raise ValidationError("Por favor, seleccione un archivo CSV.")
        
        try:
            # Decodificar archivo
            file_content = base64.b64decode(self.import_file)
            
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            file_text = None
            
            for encoding in encodings:
                try:
                    file_text = file_content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if file_text is None:
                raise ValidationError("No se pudo decodificar el archivo. Verifique el formato.")
            
            # Configurar CSV reader
            csv_reader = csv.DictReader(
                io.StringIO(file_text),
                delimiter=self.delimiter
            )
            
            # Crear registro de importación
            packing_list_name = self.packing_list_name or f'Packing List - {self.purchase_order_id.name}'
            
            packing_list = self.env['packing.list.import'].create({
                'name': packing_list_name,
                'purchase_order_id': self.purchase_order_id.id,
                'container_number': self.container_number,
                'commercial_invoice': self.commercial_invoice,
                'state': 'draft',
                'import_date': fields.Datetime.now(),
            })
            
            # Procesar líneas
            lines_data = []
            line_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start=2 porque la primera es header
                try:
                    line_data = self._process_csv_row(row, row_num)
                    if line_data:
                        line_data['packing_list_id'] = packing_list.id
                        lines_data.append(line_data)
                        line_count += 1
                except Exception as e:
                    errors.append(f"Línea {row_num}: {str(e)}")
            
            if not lines_data:
                raise ValidationError("No se encontraron datos válidos para importar.")
            
            # Crear líneas
            self.env['packing.list.import.line'].create(lines_data)
            
            # Actualizar estado
            packing_list.state = 'imported'
            
            # Preparar mensaje de resultado
            message = f"Importación completada:\n"
            message += f"- {line_count} líneas importadas\n"
            if errors:
                message += f"- {len(errors)} errores encontrados\n"
                message += "\nErrores:\n" + "\n".join(errors[:10])  # Mostrar solo los primeros 10
            
            # Retornar vista del packing list
            return {
                'type': 'ir.actions.act_window',
                'name': 'Packing List Importado',
                'res_model': 'packing.list.import',
                'res_id': packing_list.id,
                'view_mode': 'form',
                'target': 'current',
                'context': {
                    'form_view_initial_mode': 'edit',
                    'import_message': message
                }
            }
            
        except Exception as e:
            raise ValidationError(f"Error al procesar el archivo CSV: {str(e)}")
    
    def _process_csv_row(self, row, row_num):
        """
        Procesar una fila del CSV
        
        Formato esperado (ajustable):
        - product_name: Nombre del material
        - height: Alto en cm
        - width: Ancho en cm  
        - thickness: Grosor en cm
        - lot: Lote personalizado
        - wooden_crate: Código de atado/wooden crate
        - supplier_lot: Número de lote del proveedor
        - cost: Costo unitario
        - price_per_sqm: Precio por m²
        - finish: Acabado (opcional)
        """
        try:
            # Limpiar y validar datos
            product_name = self._clean_field(row.get('product_name') or row.get('Product Name') or row.get('Material'), 'product_name', row_num)
            height = self._parse_float(row.get('height') or row.get('Height') or row.get('Alto'), 'height', row_num)
            width = self._parse_float(row.get('width') or row.get('Width') or row.get('Ancho'), 'width', row_num)
            thickness = self._parse_float(row.get('thickness') or row.get('Thickness') or row.get('Grosor'), 'thickness', row_num)
            lot = self._clean_field(row.get('lot') or row.get('Lot') or row.get('Lote'), 'lot', row_num)
            wooden_crate = self._clean_field(row.get('wooden_crate') or row.get('Wooden Crate') or row.get('Crate'), 'wooden_crate', row_num)
            supplier_lot = self._clean_field(row.get('supplier_lot') or row.get('Supplier Lot') or row.get('Lot Number'), 'supplier_lot', row_num)
            
            # Campos opcionales
            cost = self._parse_float(row.get('cost') or row.get('Cost') or row.get('Costo'), 'cost', row_num, required=False)
            price_per_sqm = self._parse_float(row.get('price_per_sqm') or row.get('Price per SQM'), 'price_per_sqm', row_num, required=False)
            finish = self._clean_field(row.get('finish') or row.get('Finish') or row.get('Acabado'), 'finish', row_num, required=False)
            
            return {
                'product_name': product_name,
                'marble_height': height,
                'marble_width': width,
                'marble_thickness': thickness,
                'marble_custom_lot': lot,
                'wooden_crate_code': wooden_crate,
                'supplier_lot_number': supplier_lot,
                'cost_price': cost or 0.0,
                'price_per_sqm': price_per_sqm or 0.0,
                'marble_finish': finish or '',
            }
            
        except ValueError as e:
            raise ValidationError(f"Error en formato de datos: {str(e)}")
    
    def _clean_field(self, value, field_name, row_num, required=True):
        """Limpiar y validar campo de texto"""
        if not value or str(value).strip() == '':
            if required:
                raise ValueError(f"Campo requerido '{field_name}' vacío en línea {row_num}")
            return ''
        return str(value).strip()
    
    def _parse_float(self, value, field_name, row_num, required=True):
        """Parsear y validar campo numérico"""
        if not value or str(value).strip() == '':
            if required:
                raise ValueError(f"Campo numérico requerido '{field_name}' vacío en línea {row_num}")
            return 0.0
        
        try:
            # Limpiar el valor (remover espacios, comas como separadores de miles)
            clean_value = str(value).strip().replace(',', '')
            return float(clean_value)
        except (ValueError, TypeError):
            raise ValueError(f"Valor inválido para '{field_name}' en línea {row_num}: '{value}'")
    
    def _import_from_excel(self):
        """Importar desde archivo Excel"""
        raise UserError("Importación desde Excel no implementada aún. Use CSV por favor.")
    
    def _import_from_manual(self):
        """Importar desde datos manuales en JSON"""
        if not self.manual_data:
            raise ValidationError("Por favor, ingrese los datos manuales en formato JSON.")
        
        try:
            data = json.loads(self.manual_data)
            
            if not isinstance(data, list):
                raise ValidationError("Los datos deben ser una lista de objetos JSON.")
            
            # Crear registro de importación
            packing_list_name = self.packing_list_name or f'Packing List Manual - {self.purchase_order_id.name}'
            
            packing_list = self.env['packing.list.import'].create({
                'name': packing_list_name,
                'purchase_order_id': self.purchase_order_id.id,
                'container_number': self.container_number,
                'commercial_invoice': self.commercial_invoice,
                'state': 'draft',
                'import_date': fields.Datetime.now(),
            })
            
            # Procesar líneas
            lines_data = []
            for i, item in enumerate(data, 1):
                try:
                    line_data = self._process_manual_item(item, i)
                    line_data['packing_list_id'] = packing_list.id
                    lines_data.append(line_data)
                except Exception as e:
                    raise ValidationError(f"Error en elemento {i}: {str(e)}")
            
            # Crear líneas
            self.env['packing.list.import.line'].create(lines_data)
            
            # Actualizar estado
            packing_list.state = 'imported'
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Packing List Importado',
                'res_model': 'packing.list.import',
                'res_id': packing_list.id,
                'view_mode': 'form',
                'target': 'current'
            }
            
        except json.JSONDecodeError:
            raise ValidationError("Error en formato JSON. Verifique la sintaxis.")
        except Exception as e:
            raise ValidationError(f"Error al procesar los datos manuales: {str(e)}")
    
    def _process_manual_item(self, item, item_num):
        """Procesar un elemento JSON manual"""
        required_fields = ['product_name', 'marble_height', 'marble_width', 'marble_thickness', 
                          'marble_custom_lot', 'wooden_crate_code', 'supplier_lot_number']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in item or not item[field]:
                raise ValueError(f"Campo requerido '{field}' faltante o vacío")
        
        # Validar tipos de datos
        numeric_fields = ['marble_height', 'marble_width', 'marble_thickness', 'cost_price', 'price_per_sqm']
        for field in numeric_fields:
            if field in item and item[field] is not None:
                try:
                    item[field] = float(item[field])
                except (ValueError, TypeError):
                    raise ValueError(f"Valor inválido para campo numérico '{field}': {item[field]}")
        
        return item
    
    def action_generate_template(self):
        """Generar archivo CSV de plantilla"""
        self.ensure_one()
        
        # Crear CSV de ejemplo
        csv_content = '''product_name,height,width,thickness,lot,wooden_crate,supplier_lot,cost,price_per_sqm,finish
Amazon-2cm-Leather,320.5,160.2,2.0,BD00172535,BD00172535,204952-031,150.00,75.00,Leather
Metalicus-2cm-Polished,305.0,155.8,2.0,BD00172535,BD00172535,204952-032,180.00,90.00,Polished
Carrara-3cm-Honed,280.3,140.6,3.0,BD00173210,BD00173210,205464-019,200.00,66.67,Honed'''
        
        # Codificar a base64
        csv_encoded = base64.b64encode(csv_content.encode('utf-8'))
        
        # Crear attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'packing_list_template.csv',
            'type': 'binary',
            'datas': csv_encoded,
            'mimetype': 'text/csv',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
    
    def action_show_json_example(self):
        """Mostrar ejemplo de formato JSON"""
        json_example = '''[
    {
        "product_name": "Amazon-2cm-Leather",
        "marble_height": 320.5,
        "marble_width": 160.2,
        "marble_thickness": 2.0,
        "marble_custom_lot": "BD00172535",
        "wooden_crate_code": "BD00172535",
        "supplier_lot_number": "204952-031",
        "cost_price": 150.00,
        "price_per_sqm": 75.00,
        "marble_finish": "Leather"
    },
    {
        "product_name": "Metalicus-2cm-Polished",
        "marble_height": 305.0,
        "marble_width": 155.8,
        "marble_thickness": 2.0,
        "marble_custom_lot": "BD00172535", 
        "wooden_crate_code": "BD00172535",
        "supplier_lot_number": "204952-032",
        "cost_price": 180.00,
        "price_per_sqm": 90.00,
        "marble_finish": "Polished"
    }
]'''
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ejemplo de Formato JSON',
            'res_model': 'packing.list.import.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_manual_data': json_example,
                'show_json_example': True
            }
        }