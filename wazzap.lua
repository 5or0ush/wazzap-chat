-- Wazzap simple text protocol
local p_wazzap = Proto("wazzap","Wazzap Chat")

local f_type = ProtoField.string("wazzap.type","Type")
local f_time = ProtoField.string("wazzap.time","Time")
local f_user = ProtoField.string("wazzap.user","User")
local f_text = ProtoField.string("wazzap.text","Text")
p_wazzap.fields = {f_type,f_time,f_user,f_text}

local function parse_first_line(s)
  local line = s:match("([^\r\n]+)")
  if not line then return nil end
  if line:sub(1,4) == "SYS:" then
    return {type="SYS", text=line:sub(5)}
  else
    -- formats:
    -- "HH:MM:SS user: text"  (if you later add timestamps)
    -- "user: text"
    local ts,u,txt = line:match("^(%d%d:%d%d:%d%d)%s+([^:]+):%s*(.*)$")
    if ts then return {type="MSG", time=ts, user=u, text=txt} end
    local u2,txt2 = line:match("^([^:]+):%s*(.*)$")
    if u2 then return {type="MSG", user=u2, text=txt2} end
  end
  return {type="RAW", text=line}
end

function p_wazzap.dissector(buf,pinfo,tree)
  local data = buf():string()
  if not data or #data == 0 then return end
  local parsed = parse_first_line(data)
  if not parsed then return end
  pinfo.cols.protocol = "WAZZAP"
  local t = tree:add(p_wazzap, buf(), "Wazzap Chat")
  t:add(f_type, parsed.type or "")
  if parsed.time then t:add(f_time, parsed.time) end
  if parsed.user then t:add(f_user, parsed.user) end
  if parsed.text then t:add(f_text, parsed.text) end
end

-- Bind to your server port (change if needed)
local tcp_port = DissectorTable.get("tcp.port")
tcp_port:add(12345, p_wazzap)