import os
import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path


class AIEnhancer:
    def __init__(self):
        self.session = None
        self.is_processing = False
        self.cancel_flag = False
        self.input_size = 64
        self.scale_factor = 4
        self.denoise_strength = 5

    def load_model(self, model_type: str = "general"):
        print("🔄 Загружаю модель...")

        # Ищем модель
        project_dir = Path(__file__).resolve().parent.parent
        model_path = project_dir / "models" / "RealESRGAN_x4.onnx"

        if not model_path.exists():
            raise FileNotFoundError(f"Модель не найдена: {model_path}")

        # Провайдеры (DirectML для GPU через DirectX)
        available_providers = ort.get_available_providers()
        print(f"Доступные провайдеры: {available_providers}")

        if 'DmlExecutionProvider' in available_providers:
            providers = ['DmlExecutionProvider', 'CPUExecutionProvider']
            print("🎮 Используем GPU (DirectML)")
        elif 'CUDAExecutionProvider' in available_providers:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print("🎮 Используем GPU (CUDA)")
        else:
            providers = ['CPUExecutionProvider']
            print("💻 Используем CPU")

        # Создаём сессию
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.session = ort.InferenceSession(
            str(model_path),
            sess_options=sess_options,
            providers=providers
        )

        # Определяем размер входа
        input_shape = self.session.get_inputs()[0].shape
        self.input_size = input_shape[2] if isinstance(input_shape[2], int) else 64

        print(f"✅ Модель загружена: {model_path.name}")
        print(f"📊 Размер тайла: {self.input_size}x{self.input_size}")
        print(f"🎮 Активные провайдеры: {self.session.get_providers()}\n")

    def set_denoise_strength(self, strength):
        """Устанавливает силу предварительного шумоподавления"""
        self.denoise_strength = int(strength)

    def _process_tile(self, tile_rgb):
        """Обрабатывает один тайл"""
        h, w = tile_rgb.shape[:2]
        if h != self.input_size or w != self.input_size:
            padded = np.zeros((self.input_size, self.input_size, 3), dtype=np.uint8)
            padded[:min(h, self.input_size), :min(w, self.input_size)] = tile_rgb[
                :min(h, self.input_size), :min(w, self.input_size)]
            tile_rgb = padded

        tile_float = tile_rgb.astype(np.float32) / 255.0
        tile_nchw = np.expand_dims(np.transpose(tile_float, (2, 0, 1)), axis=0)

        input_name = self.session.get_inputs()[0].name
        output = self.session.run(None, {input_name: tile_nchw})[0]

        output_hwc = np.transpose(output[0], (1, 2, 0))
        output_uint8 = np.clip(output_hwc * 255.0, 0, 255.0).astype(np.uint8)
        return output_uint8

    def enhance_image(self, input_path, output_path, scale=2, progress_callback=None):
        if not self.session:
            return {"success": False, "error": "Модель не загружена!"}

        self.is_processing = True
        self.cancel_flag = False

        try:
            if progress_callback:
                progress_callback(5, "Загрузка изображения...")

            # Чтение через numpy (поддержка кириллицы в путях)
            img_data = np.fromfile(input_path, dtype=np.uint8)
            img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
            if img is None:
                return {"success": False, "error": "Не удалось прочитать изображение"}

            h, w = img.shape[:2]
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Предварительное шумоподавление (перед нейросетью)
            if self.denoise_strength > 0:
                if progress_callback:
                    progress_callback(8, f"Шумоподавление (сила: {self.denoise_strength})...")
                img_rgb = cv2.fastNlMeansDenoisingColored(
                    img_rgb, None,
                    h=self.denoise_strength,
                    hColor=self.denoise_strength,
                    templateWindowSize=7,
                    searchWindowSize=21
                )

            if progress_callback:
                progress_callback(10, "Подготовка тайлов...")

            tile_size = self.input_size
            out_h = h * self.scale_factor
            out_w = w * self.scale_factor
            output_buffer = np.zeros((out_h, out_w, 3), dtype=np.uint8)

            tiles_y = (h + tile_size - 1) // tile_size
            tiles_x = (w + tile_size - 1) // tile_size
            total_tiles = tiles_y * tiles_x
            processed_tiles = 0

            if progress_callback:
                progress_callback(15, f"Обработка: 0/{total_tiles} тайлов")

            for y in range(0, h, tile_size):
                for x in range(0, w, tile_size):
                    if self.cancel_flag:
                        return {"success": False, "error": "Обработка отменена"}

                    y2 = min(y + tile_size, h)
                    x2 = min(x + tile_size, w)
                    tile = img_rgb[y:y2, x:x2]

                    out_tile = self._process_tile(tile)

                    tile_h = y2 - y
                    tile_w = x2 - x
                    out_tile = out_tile[:tile_h * self.scale_factor, :tile_w * self.scale_factor]

                    oy1 = y * self.scale_factor
                    ox1 = x * self.scale_factor
                    oy2 = oy1 + out_tile.shape[0]
                    ox2 = ox1 + out_tile.shape[1]

                    output_buffer[oy1:oy2, ox1:ox2] = out_tile

                    processed_tiles += 1
                    if progress_callback and processed_tiles % 5 == 0:
                        percent = 15 + int((processed_tiles / total_tiles) * 70)
                        progress_callback(percent, f"Обработка: {processed_tiles}/{total_tiles} тайлов")

            if progress_callback:
                progress_callback(85, "Финализация...")

            if scale == 1:
                output_buffer = cv2.resize(output_buffer, (w, h), interpolation=cv2.INTER_AREA)
            elif scale == 2:
                output_buffer = cv2.resize(output_buffer, (w * 2, h * 2), interpolation=cv2.INTER_AREA)

            output_bgr = cv2.cvtColor(output_buffer, cv2.COLOR_RGB2BGR)

            if progress_callback:
                progress_callback(95, "Сохранение...")

            # Сохранение через numpy (поддержка кириллицы в путях)
            ext = os.path.splitext(output_path)[1]
            is_success, buffer = cv2.imencode(ext, output_bgr, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            if is_success:
                buffer.tofile(output_path)
            else:
                return {"success": False, "error": "Не удалось сохранить изображение"}

            if progress_callback:
                progress_callback(100, "Готово!")

            return {"success": True, "output_path": output_path,
                    "original_size": os.path.getsize(input_path), "new_size": os.path.getsize(output_path)}

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
        finally:
            self.is_processing = False

    def cancel(self):
        if self.is_processing:
            self.cancel_flag = True
            print("🛑 Отмена...")


ai_enhancer = AIEnhancer()