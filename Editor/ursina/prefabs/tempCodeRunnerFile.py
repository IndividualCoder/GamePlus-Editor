                elif isinstance(self.partKey, list):
                    if self.on_key_press and self.Key is not None and key == self.Key and all(held_keys[key] for key in self.partKey):
                        self.on_key_press()
