#coding:utf-8
<html>
<head>
<title>出(入)库单</title>
  <style type='text/css'>
    @media print{
    .header-table,.content-table{
      width : 100%;
      border-collapse : collapse;
    }
    .header-table,.header-table td{ 
      border : none;
    }
    .content-table th,.content-table td{
      border : 1px solid #000;
    }
    .content-table tfoot td{
      border : none;
    }
}
  </style>
</head>
<body>

%for picking in objects:
<table class='header-table'>
  <tr>
    <th colspan='4'>${user.company_id.name}
      %if picking.type=='in':
        入库单
      %endif
      %if picking.type=='out':
        出库单
      %endif
      %if picking.type=='internal':
        调拨单
      %endif
    </th>
  </tr>
  <tr>
    <td>库单号:</td>
    <td>${picking.name}</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>客户/供货商:</td>
    <td colspan='2'>${picking.partner_id.name or ''|entity}</td>
  </tr>
  <tr>
    <td>录入时间:</td>
    <td>${formatLang(picking.date,date_time = True)}</td>
    <td>确认时间:</td>
    <td>${formatLang(picking.date_done,date_time = True) or ''|entity}</td>
  </tr>
</table>
<table class='content-table'>
  <thead>
    <tr>
      <th>物品名称</th>
      <th>物品编码</th>
      <th>单位</th>
      <th>数量</th>
      <th>源库位</th>
      <th>目标库位</th>
    </tr>
  </thead>
  <tbody>
    %for line in  picking.move_lines:
    <tr>
      <td>${line.product_id.name}</td>
      <td>${line.product_id.default_code}</td>
      <td>${line.product_uom.name}</td>
      <td>${line.product_qty}</td>
      <td>${line.location_id.name or ''|entity}</td>
      <td>${picking.location_dest_id.name or ''|entity}</td>
    </tr>
    %endfor
  </tbody>
  <tfoot>
    <tr>
      <td>制表人:</td>
      <td colspan='3'>${user.name}</td>
      <td>复核人:</td>
      <td colspan='2'></td>
    </tr>
  </tfoot>
</table>
%endfor
</body>
</html>
