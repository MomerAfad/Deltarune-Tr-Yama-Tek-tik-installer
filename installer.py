import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import winreg
from pathlib import Path
import platform


class DeltarunePatchInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluesoul DELTARUNE Chapter 3-4 Türkçe yama")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Dark theme colors
        self.bg_color = "#1e2431"
        self.fg_color = "#ffffff"
        self.secondary_bg = "#2a3142"
        self.accent_blue = "#2d5aff"
        self.button_dark = "#343a4d"
        self.gray_text = "#8a92a8"
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Set window icon
        try:
            icon_path = Path(__file__).parent / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass  # If icon fails to load, continue without it
        
        # Patch directory (bundled with installer)
        self.patch_dir = Path(__file__).parent / "DeltaruneTRpatch"
        self.deltarune_path = None
        self.patch_version = "1.0"
        
        self.create_widgets()
        self.auto_detect_deltarune()
        
    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=60, pady=40)
        
        # Title
        title_label = tk.Label(
            main_container,
            text="Bluesoul DELTARUNE Chapter 3-4 Türkçe yama",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 40))
        
        # Status info frame
        status_info_frame = tk.Frame(main_container, bg=self.bg_color)
        status_info_frame.pack(fill="x", pady=(0, 10))
        
        self.durum_label = tk.Label(
            status_info_frame,
            text="Durum: İndirmeye hazır.",
            font=("Segoe UI", 11),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        self.durum_label.pack(anchor="w")
        
        # Status message
        self.status_label = tk.Label(
            status_info_frame,
            text="İndirmeye hazır.",
            font=("Segoe UI", 11),
            bg=self.bg_color,
            fg=self.gray_text,
            anchor="w"
        )
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        # Progress bar with custom style
        progress_frame = tk.Frame(main_container, bg=self.secondary_bg, height=8)
        progress_frame.pack(fill="x", pady=(20, 0))
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.secondary_bg,
            background=self.gray_text,
            bordercolor=self.secondary_bg,
            lightcolor=self.gray_text,
            darkcolor=self.gray_text,
            thickness=8
        )
        
        self.progress = ttk.Progressbar(
            main_container,
            mode='determinate',
            length=780,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(15, 30))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_container, bg=self.bg_color)
        buttons_frame.pack(pady=20)
        
        # Install button (Yamayı İndir)
        self.install_btn = tk.Button(
            buttons_frame,
            text="Yamayı İndir",
            command=self.install_patch,
            bg=self.accent_blue,
            fg=self.fg_color,
            font=("Segoe UI", 12, "bold"),
            width=32,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground="#3d6aff",
            activeforeground=self.fg_color,
            bd=0
        )
        self.install_btn.pack(pady=(0, 15))
        
        # Browse button (Oyun Konumunu Seç)
        self.browse_btn = tk.Button(
            buttons_frame,
            text="Oyun Konumunu Seç",
            command=self.browse_path,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 11),
            width=32,
            height=2,
            relief="solid",
            cursor="hand2",
            bd=1,
            highlightthickness=1,
            highlightbackground=self.button_dark,
            activebackground=self.button_dark,
            activeforeground=self.fg_color
        )
        self.browse_btn.pack(pady=(0, 15))
        
        # Remove patch button (Yamayı Kaldır)
        self.remove_btn = tk.Button(
            buttons_frame,
            text="Yamayı Kaldır (Orijinale Dön)",
            command=self.remove_patch,
            bg=self.button_dark,
            fg=self.fg_color,
            font=("Segoe UI", 10),
            width=32,
            height=2,
            relief="solid",
            cursor="hand2",
            bd=1,
            highlightthickness=1,
            highlightbackground="#5a5f72",
            activebackground="#4a4f62",
            activeforeground=self.fg_color
        )
        self.remove_btn.pack()
        
        # Bottom status
        bottom_frame = tk.Frame(main_container, bg=self.bg_color)
        bottom_frame.pack(side="bottom", fill="x", pady=(40, 0))
        
        self.action_label = tk.Label(
            bottom_frame,
            text="Eylem bekleniyor...",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.gray_text
        )
        self.action_label.pack()
        
        # Globe icon (using unicode character)
        globe_label = tk.Label(
            bottom_frame,
            text="🌐",
            font=("Segoe UI", 14),
            bg=self.bg_color,
            fg=self.gray_text
        )
        globe_label.pack(pady=(10, 5))
        
        # Version
        version_label = tk.Label(
            bottom_frame,
            text=f"Yama Sürümü: {self.patch_version}",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.gray_text
        )
        version_label.pack()
        
    def auto_detect_deltarune(self):
        """Auto-detect Deltarune installation path"""
        self.action_label.config(text="Oyun konumu aranıyor...")
        self.status_label.config(text="Arama yapılıyor...")
        self.root.update()
        
        possible_paths = []
        
        if platform.system() == "Windows":
            # Check Steam library paths
            try:
                # Default Steam path
                steam_paths = [
                    r"C:\Program Files (x86)\Steam\steamapps\common\Deltarune",
                    r"C:\Program Files\Steam\steamapps\common\Deltarune",
                ]
                
                # Try to read Steam library folders from registry
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
                    steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
                    winreg.CloseKey(key)
                    steam_paths.append(os.path.join(steam_path, "steamapps", "common", "Deltarune"))
                except:
                    pass
                
                possible_paths.extend(steam_paths)
                
                # Check common game directories
                drives = ['C:', 'D:', 'E:']
                for drive in drives:
                    possible_paths.append(f"{drive}\\Games\\Deltarune")
                    possible_paths.append(f"{drive}\\Deltarune")
                    
            except Exception as e:
                print(f"Error checking Windows paths: {e}")
                
        elif platform.system() == "Linux":
            # Check common Linux Steam paths
            home = Path.home()
            possible_paths.extend([
                home / ".steam" / "steam" / "steamapps" / "common" / "Deltarune",
                home / ".local" / "share" / "Steam" / "steamapps" / "common" / "Deltarune",
            ])
        
        # Check if any path exists and contains DELTARUNE.exe or similar
        for path in possible_paths:
            path_obj = Path(path)
            if path_obj.exists():
                # Check for game executable
                if (path_obj / "DELTARUNE.exe").exists() or (path_obj / "SURVEY_PROGRAM.exe").exists():
                    self.deltarune_path = str(path_obj)
                    self.durum_label.config(text="Durum: Oyun bulundu, yama hazır!")
                    self.status_label.config(text=f"Konum: {self.deltarune_path}")
                    self.action_label.config(text="Yamayı kurmak için 'Yamayı İndir' butonuna tıklayın")
                    return
        
        # Not found
        self.durum_label.config(text="Durum: Oyun konumu bulunamadı")
        self.status_label.config(text="'Oyun Konumunu Seç' butonuna tıklayarak manuel seçin")
        self.action_label.config(text="Eylem bekleniyor...")
        
    def browse_path(self):
        """Let user browse for Deltarune installation folder"""
        folder = filedialog.askdirectory(title="Deltarune Kurulum Klasörünü Seçin")
        if folder:
            path_obj = Path(folder)
            # Verify it's a valid Deltarune directory
            if (path_obj / "DELTARUNE.exe").exists() or (path_obj / "SURVEY_PROGRAM.exe").exists():
                self.deltarune_path = folder
                self.durum_label.config(text="Durum: Oyun konumu seçildi!")
                self.status_label.config(text=f"Konum: {folder}")
                self.action_label.config(text="Yamayı kurmak için 'Yamayı İndir' butonuna tıklayın")
            else:
                self.durum_label.config(text="Durum: Hata!")
                self.status_label.config(text="Geçersiz klasör seçildi")
                self.action_label.config(text="Eylem bekleniyor...")
                messagebox.showerror(
                    "Hata",
                    "Seçilen klasör geçerli bir Deltarune kurulum klasörü değil!\n"
                    "DELTARUNE.exe veya SURVEY_PROGRAM.exe dosyası bulunamadı."
                )
                
    def install_patch(self):
        """Install the Turkish patch"""
        if not self.deltarune_path:
            self.durum_label.config(text="Durum: Hata!")
            self.status_label.config(text="Oyun konumu seçilmedi")
            self.action_label.config(text="Lütfen oyun konumunu seçin")
            messagebox.showerror("Hata", "Lütfen önce Deltarune kurulum klasörünü seçin!")
            return
            
        if not self.patch_dir.exists():
            self.durum_label.config(text="Durum: Hata!")
            self.status_label.config(text="Yama dosyaları bulunamadı")
            messagebox.showerror("Hata", "Yama dosyaları bulunamadı!\nDeltaruneTRpatch klasörü mevcut değil.")
            return
        
        try:
            self.install_btn.config(state="disabled")
            self.browse_btn.config(state="disabled")
            self.remove_btn.config(state="disabled")
            
            self.durum_label.config(text="Durum: Yükleniyor...")
            self.action_label.config(text="Yama kuruluyor...")
            self.progress['value'] = 0
            self.root.update()
            
            deltarune_path = Path(self.deltarune_path)
            
            # Create backup
            backup_dir = deltarune_path / "backup_original"
            if not backup_dir.exists():
                self.status_label.config(text="Orijinal dosyalar yedekleniyor...")
                backup_dir.mkdir(exist_ok=True)
                
                # Backup data.win if exists
                if (deltarune_path / "data.win").exists():
                    shutil.copy2(deltarune_path / "data.win", backup_dir / "data.win")
            
            self.progress['value'] = 30
            self.root.update()
            
            # Copy patch files
            self.status_label.config(text="Yama dosyaları kopyalanıyor...")
            
            files_to_copy = []
            
            # Copy data.win
            if (self.patch_dir / "data.win").exists():
                files_to_copy.append(("data.win", deltarune_path))
            
            # Copy chapter folders
            for chapter_dir in self.patch_dir.glob("chapter*"):
                if chapter_dir.is_dir():
                    files_to_copy.append((chapter_dir.name, deltarune_path))
            
            # Copy mus folder
            if (self.patch_dir / "mus").exists():
                files_to_copy.append(("mus", deltarune_path))
            
            progress_step = 60 / len(files_to_copy) if files_to_copy else 0
            
            for item, dest_parent in files_to_copy:
                source = self.patch_dir / item
                dest = dest_parent / item
                
                if source.is_file():
                    shutil.copy2(source, dest)
                else:
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(source, dest)
                
                self.progress['value'] += progress_step
                self.root.update()
            
            self.progress['value'] = 100
            self.durum_label.config(text="Durum: Tamamlandı!")
            self.status_label.config(text="Yama başarıyla kuruldu!")
            self.action_label.config(text="Kurulum tamamlandı. İyi oyunlar!")
            
            messagebox.showinfo(
                "Başarılı",
                "Deltarune Türkçe yaması başarıyla kuruldu!\n\n"
                "Orijinal dosyalar 'backup_original' klasöründe yedeklendi.\n"
                "Artık oyunu Türkçe oynayabilirsiniz!"
            )
            
        except Exception as e:
            self.durum_label.config(text="Durum: Hata!")
            self.status_label.config(text="Yama kurulumu başarısız oldu!")
            self.action_label.config(text="Bir hata oluştu")
            messagebox.showerror("Hata", f"Yama kurulumu sırasında bir hata oluştu:\n{str(e)}")
        
        finally:
            self.install_btn.config(state="normal")
            self.browse_btn.config(state="normal")
            self.remove_btn.config(state="normal")
    
    def remove_patch(self):
        """Remove the Turkish patch and restore original files"""
        if not self.deltarune_path:
            self.durum_label.config(text="Durum: Hata!")
            self.status_label.config(text="Oyun konumu seçilmedi")
            self.action_label.config(text="Lütfen oyun konumunu seçin")
            messagebox.showerror("Hata", "Lütfen önce Deltarune kurulum klasörünü seçin!")
            return
        
        deltarune_path = Path(self.deltarune_path)
        backup_dir = deltarune_path / "backup_original"
        
        if not backup_dir.exists():
            self.durum_label.config(text="Durum: Hata!")
            self.status_label.config(text="Yedek bulunamadı")
            self.action_label.config(text="Orijinal dosyalar bulunamadı")
            messagebox.showerror(
                "Hata", 
                "Yedek klasörü bulunamadı!\n\n"
                "Yama kurulmamış olabilir veya yedekler silinmiş olabilir."
            )
            return
        
        # Confirm removal
        confirm = messagebox.askyesno(
            "Yamayı Kaldır",
            "Türkçe yamayı kaldırıp orijinal dosyalara dönmek istediğinize emin misiniz?\n\n"
            "Bu işlem mevcut yama dosyalarını silecek ve yedeklerden geri yükleyecektir."
        )
        
        if not confirm:
            return
        
        try:
            self.install_btn.config(state="disabled")
            self.browse_btn.config(state="disabled")
            self.remove_btn.config(state="disabled")
            
            self.durum_label.config(text="Durum: Kaldırılıyor...")
            self.action_label.config(text="Yama kaldırılıyor...")
            self.progress['value'] = 0
            self.root.update()
            
            # List files to restore
            files_to_restore = []
            backup_files = list(backup_dir.iterdir())
            
            if not backup_files:
                raise Exception("Yedek klasörü boş!")
            
            self.status_label.config(text="Orijinal dosyalar geri yükleniyor...")
            self.progress['value'] = 20
            self.root.update()
            
            # Restore backed up files
            progress_step = 60 / len(backup_files) if backup_files else 0
            
            for backup_file in backup_files:
                dest = deltarune_path / backup_file.name
                
                if backup_file.is_file():
                    shutil.copy2(backup_file, dest)
                else:
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(backup_file, dest)
                
                self.progress['value'] += progress_step
                self.root.update()
            
            self.progress['value'] = 80
            self.status_label.config(text="Yama dosyaları temizleniyor...")
            self.root.update()
            
            # Remove patch-specific folders that might exist
            patch_folders = ["chapter3_windows", "chapter4_windows"]
            for folder_name in patch_folders:
                folder_path = deltarune_path / folder_name
                if folder_path.exists() and folder_path not in backup_files:
                    try:
                        shutil.rmtree(folder_path)
                    except:
                        pass
            
            self.progress['value'] = 100
            self.durum_label.config(text="Durum: Kaldırıldı!")
            self.status_label.config(text="Yama başarıyla kaldırıldı!")
            self.action_label.config(text="Orijinal dosyalar geri yüklendi")
            
            messagebox.showinfo(
                "Başarılı",
                "Türkçe yama başarıyla kaldırıldı!\n\n"
                "Orijinal dosyalar geri yüklendi.\n"
                "Artık oyunu orijinal dilinde oynayabilirsiniz.\n\n"
                "Not: 'backup_original' klasörünü güvenli bir şekilde silebilirsiniz."
            )
            
        except Exception as e:
            self.durum_label.config(text="Durum: Hata!")
            self.status_label.config(text="Yama kaldırma başarısız!")
            self.action_label.config(text="Bir hata oluştu")
            messagebox.showerror("Hata", f"Yama kaldırılırken bir hata oluştu:\n{str(e)}")
        
        finally:
            self.install_btn.config(state="normal")
            self.browse_btn.config(state="normal")
            self.remove_btn.config(state="normal")


def main():
    root = tk.Tk()
    app = DeltarunePatchInstaller(root)
    root.mainloop()


if __name__ == "__main__":
    main()
