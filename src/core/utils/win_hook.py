import os

import win32api as wapi
import win32con as wcon
import win32gui as wgui
import win32process as wproc

import src.core.utils.colors as CU


def enum_windows_proc(wnd, param):
    pid = param.get("pid", None)
    data = param.get("data", None)
    if pid is None or wproc.GetWindowThreadProcessId(wnd)[1] == pid:
        text = wgui.GetWindowText(wnd)
        if text:
            style = wapi.GetWindowLong(wnd, wcon.GWL_STYLE)
            if style & wcon.WS_VISIBLE:
                if data is not None:
                    data.append((wnd, text))


def enum_process_windows(pid=None):
    data = []
    param = {
        "pid": pid,
        "data": data,
    }
    wgui.EnumWindows(enum_windows_proc, param)
    return data


def _filter_processes(processes, search_name=None):
    if search_name is None:
        return processes
    filtered = []
    for pid, _ in processes:
        try:
            proc = wapi.OpenProcess(wcon.PROCESS_ALL_ACCESS, 0, pid)
        except:
            continue
        try:
            file_name = wproc.GetModuleFileNameEx(proc, None)
        except:
            wapi.CloseHandle(proc)
            continue
        base_name = file_name.split(os.path.sep)[-1]
        if base_name.lower() == search_name.lower():
            filtered.append((pid, file_name))
        wapi.CloseHandle(proc)
    return tuple(filtered)


def enum_processes(process_name=None):
    procs = [(pid, None) for pid in wproc.EnumProcesses()]
    return _filter_processes(procs, search_name=process_name)


def getDofusWindows(*args):
    nomPersos = []
    proc_name = args[0] if args else None
    procs = enum_processes(process_name=proc_name)
    for pid, name in procs:
        data = enum_process_windows(pid)
        if data:
            for handle, text in data:
                nomPersos.append(text)
    return nomPersos


def removeActive():
    curr = wgui.GetWindowText(wgui.GetForegroundWindow())
    dofusWindows = getDofusWindows("Dofus.exe")
    try:
        dofusWindows.pop(dofusWindows.index(curr))
        print("\nMacro enregistrée sur " + CU.bColors.WARNING + CU.bColors.BOLD + curr + CU.bColors.ENDC)
    except ValueError:
        print(CU.bColors.WARNING + CU.bColors.BOLD + "ATTENTION: Fenêtre Dofus invalide" + CU.bColors.ENDC)
    return dofusWindows


def isDofusWindow():
    curr = wgui.GetWindowText(wgui.GetForegroundWindow())
    if curr.find("Dofus") != -1:
        return True
    else:
        return False


def switchToWindow(processName):
    proc_name = "Dofus.exe"
    procs = enum_processes(process_name=proc_name)
    for pid, name in procs:
        data = enum_process_windows(pid)
        if data:
            for handle, text in data:
                if processName == text.split(" -")[0]:
                    remote_thread, _ = wproc.GetWindowThreadProcessId(handle)
                    wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
                    wgui.BringWindowToTop(handle)
