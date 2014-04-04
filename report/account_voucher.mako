##coding=utf-8
%for voucher in objects:
<table style='border-collapse : collapse;border : none;'>
    <tr><td colspan='4' style="text-align : center;border : none;"><h4>${user.company_id.name}</h4></td>
    <tr><td colspan='4' style="text-align : center;border : none;"><h3>报销凭证</h3></td></tr>
    <tr>
    <td style="width : 35mm;border : none;">单位:</td>
    <td style="width : 95mm;border : none;">${voucher.partner_id.name or ''|entity}</td>
    <td style="width : 20mm;border : none;">&nbsp;</td>
    <td style="width : 50mm;border : none;">${formatLang(voucher.date,date = True) or ''|entity}</td>
    </tr>
</table>

<table style='border-collapse : collapse;border : 1px solid #000;'>
  <thead>
    <tr>
    <th style='border : thin solid gray;width : 35mm;'>日期</th>
    <th style='border : thin solid gray;width : 95mm;'>报销内容</th>
    <th style='border : thin solid gray;width : 20mm;'>金额</th>
    <th style='border : thin solid gray;width : 50mm;'>备注</th>
    </tr>
  </thead>
  <tbody>
    %for line in voucher.line_ids:
      <tr>
        <td style='border : thin solid gray;'>${line.date_original}</td>
        <td style='border : thin solid gray;'>${line.name}</td>
        <td style='border : thin solid gray;'>${line.amount}</td>
        <td style='border : thin solid gray;'></td>
      </tr>
    %endfor
  </tbody>
  <tfoot>
    <tr>
      <td colspan="3" style='border : thin solid gray;'>
        总计人民币&nbsp;&nbsp;
        ${to_big_rmb(voucher.amount)}
      </td>
      <td style='border : thin solid gray;'>&yen;:${voucher.amount}</td>
    </tr>
  </tfoot>
</table>
<table style="border-collapse : collapse;border : none;">
    <tr>
      <td colspan="4" style="width : 190mm;border : none;">
      经 办 人:  &nbsp;&nbsp;
      店    长:  &nbsp;&nbsp;
      部门经理:  &nbsp;&nbsp;
      </td>
    </tr>

    <tr>
      <td colspan="4" style="border : none;">
      总 会 计:  &nbsp;&nbsp;
      现金出纳:  &nbsp;&nbsp;
      副总经理:  &nbsp;&nbsp;
      总 经 理:  &nbsp;&nbsp;
      </td>
    </tr>
</table>
%endfor
